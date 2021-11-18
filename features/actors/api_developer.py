import psycopg2
import requests
from faas_client import FaasClientFactory
from fusionauth.fusionauth_client import FusionAuthClient
from hasura_client import HasuraClientFactory
from softozor_graphql_client import GraphQLClient
from softozor_test_utils import host_has_port_open
from softozor_test_utils.timing import fail_after_timeout


def create_hasura_client(env_info, admin_secret):
    port = 8080
    ip = env_info.get_node_ips(node_group='cp')[0]
    endpoint = f'http://{ip}:{port}'
    assert host_has_port_open(ip, port)
    factory = HasuraClientFactory('default')

    return factory.create(endpoint, admin_secret)


def create_graphql_client(env_info, admin_secret):
    endpoint = f'http://{env_info.domain()}/v1/graphql'

    return GraphQLClient(endpoint, admin_secret)


def create_database_connections(env_info, admin_user, admin_password):
    primary_node_ip = env_info.get_node_ip_from_name('Primary')
    assert primary_node_ip is not None
    secondary_node_ip = env_info.get_node_ip_from_name(
        'Secondary')
    assert secondary_node_ip is not None

    hasura_db_name = 'hasura'
    auth_db_name = 'fusionauth'

    return {
        'primary': psycopg2.connect(
            host=primary_node_ip,
            user=admin_user,
            password=admin_password,
            database=hasura_db_name),
        'secondary': psycopg2.connect(
            host=secondary_node_ip,
            user=admin_user,
            password=admin_password,
            database=hasura_db_name),
        'hasura': psycopg2.connect(
            host=primary_node_ip,
            user=admin_user,
            password=admin_password,
            database=hasura_db_name),
        'auth': psycopg2.connect(
            host=primary_node_ip,
            user=admin_user,
            password=admin_password,
            database=auth_db_name)
    }


def create_faas_client(env_info, file_client):
    node_type = 'docker'
    node_group = 'faas'
    port = 8080
    ip = env_info.get_node_ips(node_type=node_type, node_group=node_group)[0]
    assert host_has_port_open(ip, port)
    username = file_client.read(
        env_info.env_name(),
        '/var/lib/faasd/secrets/basic-auth-user',
        node_type=node_type,
        node_group=node_group)
    password = file_client.read(
        env_info.env_name(),
        '/var/lib/faasd/secrets/basic-auth-password',
        node_type=node_type,
        node_group=node_group)
    factory = FaasClientFactory(port)

    return factory.create(ip, username, password)


def create_fusionauth_client(env_info, api_key):
    ip = env_info.get_node_ips(node_group='auth', node_type='docker')[0]
    port = 9011
    assert host_has_port_open(ip, port)
    auth_url = f'http://{ip}:{port}'

    return FusionAuthClient(api_key, auth_url)


def can_invoke_function(url, timeout_in_sec=120, period_in_sec=5):
    def invoke():
        response = requests.post(url)
        return response.status_code < 500

    return fail_after_timeout(lambda: invoke(), timeout_in_sec, period_in_sec)


class ApiDeveloper:
    def __init__(self, jelastic_clients_factory, env_info, manifest_data):
        self.__db_connections = create_database_connections(
            env_info, manifest_data['Database Admin User'], manifest_data['Database Admin Password'])
        file_client = jelastic_clients_factory.create_file_client()
        self.__faas_client = create_faas_client(
            env_info, file_client)
        self.__fusionauth_client = create_fusionauth_client(
            env_info, manifest_data['Auth Almighty API Key'])
        self.__hasura_client = create_hasura_client(
            env_info, manifest_data['Hasura Admin Secret'])
        self.__graphql_client = create_graphql_client(
            env_info, manifest_data['Hasura Admin Secret'])

    def __del__(self):
        self.__close_database_connections()

    # region Database

    def database_contains_table(self, database, table_name, timeout_in_sec=120, period_in_sec=0.1):
        def test_table():
            cursor = self.__db_connections[database].cursor()
            cursor.execute(
                """
                SELECT EXISTS (
                   SELECT FROM pg_tables
                   WHERE  tablename  = %s
                );
                """, (table_name,))
            return cursor.fetchone()[0]

        return fail_after_timeout(lambda: test_table(), timeout_in_sec, period_in_sec)

    def create_table_in_database(self, table_name, database):
        database_connection = self.__db_connections[database]
        cursor = database_connection.cursor()
        cursor.execute(
            f"""
                CREATE TABLE {table_name}(
                    id int PRIMARY KEY NOT NULL
                );
                """
        )
        database_connection.commit()

    def get_database_extensions(self, database):
        cursor = self.__db_connections[database].cursor()
        cursor.execute(
            """
            SELECT extname FROM pg_extension;
            """
        )
        fetched_rows = cursor.fetchall()

        return set(extension[0] for extension in fetched_rows)

    def get_database_schemas(self, database):
        cursor = self.__db_connections[database].cursor()
        cursor.execute(
            """
            SELECT schema_name FROM information_schema.schemata;
            """
        )
        fetched_rows = cursor.fetchall()

        return set(schema[0] for schema in fetched_rows)

    def get_database_version(self, database):
        return self.__db_connections[database].server_version

    def __close_database_connections(self):
        for connection in self.__db_connections.values():
            connection.close()

    # endregion

    # region Faas engine

    def faas_is_up(self, timeout_in_sec=300, period_in_sec=15):
        def test_is_up():
            try:
                exit_code = self.__faas_client.login()
                return exit_code == 0
            except:
                return False

        return fail_after_timeout(lambda: test_is_up(), timeout_in_sec, period_in_sec)

    def log_on_faas(self):
        return self.__faas_client.login()

    def is_function_ready(self, function_name):
        def is_ready():
            return self.__faas_client.is_ready(function_name)

        return fail_after_timeout(lambda: is_ready())

    def deploy_function(self, path_to_serverless_config, function_name, env={}):
        exit_code = self.__faas_client.deploy(
            path_to_serverless_config, function_name, env)

        if exit_code == 0:
            function_url = f'http://{self.__faas_client.endpoint}/function/{function_name}'
            return can_invoke_function(function_url)
        else:
            return False

    def invoke_function(self, function_name):
        rq = requests.post(
            f'http://{self.__faas_client.endpoint}/function/{function_name}')
        assert rq.status_code == 200, f'expected status 200, got {rq.status_code}'

        return rq.json()

    # endregion

    # region Fusionauth

    def fusionauth_is_up(self, timeout_in_sec=300, period_in_sec=15):
        def test_is_up():
            try:
                response = requests.get(
                    f'{self.__fusionauth_client.base_url}/api/status')
                return response.status_code == 200
            except:
                return False

        return fail_after_timeout(lambda: test_is_up(), timeout_in_sec, period_in_sec)

    def create_user(self, user):
        response = self.__fusionauth_client.create_user({
            'sendSetPasswordEmail': False,
            'user': {
                'email': user['email'],
                'password': user['password']
            }
        })
        assert response.was_successful() is True, \
            f'unable to create user: {response.exception} ({response.status})'
        return response.success_response['user']['id']

    def register_user(self, user_id, app_id, roles):
        response = self.__fusionauth_client.register({
            'registration': {
                'applicationId': app_id,
                'roles': roles
            }
        }, user_id)
        assert response.was_successful() is True, \
            f'cannot register user with id <{user_id}> on application <{app_id}>: {response.exception} ({response.status})'

    def delete_registration(self, user_id, app_id):
        response = self.__fusionauth_client.delete_registration(
            user_id, app_id)
        assert response.was_successful() is True, \
            f'cannot unregister user id <{user_id}> from app id <{app_id}>: {response.exception} ({response.status})'

    def retrieve_user(self, user_id):
        response = self.__fusionauth_client.retrieve_user(user_id)
        assert response.was_successful() is True, \
            f'cannot retrieve user with id <{user_id}>: {response.exception} ({response.status})'
        return response.success_response['user']

    def retrieve_user_by_email(self, email):
        response = self.__fusionauth_client.retrieve_user_by_email(email)
        assert response.was_successful() is True, \
            f'cannot find user with email {email}'
        return response.success_response['user']

    def check_user_is_registered_on_application(self, user_id, app_id):
        response = self.__fusionauth_client.retrieve_registration(
            user_id, app_id)
        assert response.was_successful() is True, \
            f'cannot find registration of user {user_id} on application {app_id}'

    def delete_user(self, user_id):
        response = self.__fusionauth_client.delete_user(user_id)
        assert response.was_successful() is True, \
            f'cannot remove user with id <{user_id}>: {response.exception} ({response.status})'

    # endregion

    # region Hasura

    def hasura_is_up(self, timeout_in_sec=300, period_in_sec=15):
        def test_is_up():
            try:
                response = requests.get(
                    f'{self.__hasura_client.endpoint}/healthz')
                return response.status_code == 200
            except:
                return False

        return fail_after_timeout(lambda: test_is_up(), timeout_in_sec, period_in_sec)

    def post_graphql(self, query, variables, run_as_admin):
        response, _ = self.__graphql_client.execute(
            query=query, variables=variables, run_as_admin=run_as_admin)
        assert 'errors' not in response, f'errors: {response}'
        return response['data']

    # endregion
