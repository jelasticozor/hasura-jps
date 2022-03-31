import json
import os

import psycopg2
import requests
import yaml
from faas_client import FaasClientFactory
from fusionauth.fusionauth_client import FusionAuthClient
from hasura_client import HasuraClientFactory
from softozor_graphql_client import GraphQLClient
from softozor_test_utils import host_has_port_open
from softozor_test_utils.timing import fail_after_timeout
from test_utils.manifest_data import get_manifest_data


def create_hasura_client(env_info, admin_secret):
    port = 8080
    ip = env_info.get_node_ips(node_group='cp')[0]
    endpoint = f'http://{ip}:{port}'
    assert host_has_port_open(ip, port), \
        f'hasura port {port} not open on ip {ip}'
    factory = HasuraClientFactory('default')

    return factory.create(endpoint, admin_secret)


def create_database_connections(env_info, admin_user, admin_password):
    primary_node_ip = env_info.get_node_ip_from_name('Primary')
    assert primary_node_ip is not None, \
        f'expected primary node ip to be defined'
    secondary_node_ip = env_info.get_node_ip_from_name(
        'Secondary')
    assert secondary_node_ip is not None, \
        f'expected secondary node ip to be defined'

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
    assert host_has_port_open(ip, port), \
        f'faas port {port} not open on ip {ip}'
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
    assert host_has_port_open(ip, port), \
        f'fusionauth port {port} not open on ip {ip}'
    auth_url = f'http://{ip}:{port}'

    return FusionAuthClient(api_key, auth_url)


def can_invoke_function(url, timeout_in_sec=120, period_in_sec=5):
    def invoke():
        response = requests.post(url)
        return response.status_code < 500

    return fail_after_timeout(lambda: invoke(), timeout_in_sec, period_in_sec)


class ApiDeveloper:
    def __init__(self, jelastic_clients_factory, env_info, manifest_data, add_application_manifest_file,
                 remove_application_manifest_file, path_to_graphql_folder):
        self.__env_info = env_info
        self.__add_application_manifest_file = add_application_manifest_file
        self.__remove_application_manifest_file = remove_application_manifest_file
        self.__manifest_data = manifest_data
        self.__db_connections = create_database_connections(
            env_info, manifest_data['Database Admin User'], manifest_data['Database Admin Password'])
        self.__file_client = jelastic_clients_factory.create_file_client()
        self.__jps_client = jelastic_clients_factory.create_jps_client()
        self.__control_client = jelastic_clients_factory.create_control_client()
        self.__faas_client = create_faas_client(
            env_info, self.__file_client)
        self.__fusionauth_client = create_fusionauth_client(
            env_info, manifest_data['Auth Almighty API Key'])
        hasura_admin_secret = manifest_data['Hasura Admin Secret']
        self.__hasura_client = create_hasura_client(
            env_info, hasura_admin_secret)
        self.__path_to_graphql_folder = path_to_graphql_folder
        self.__graphql_client = GraphQLClient(
            endpoint=f'https://{env_info.domain()}/v1/graphql', admin_secret=hasura_admin_secret)

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

    def retrieve_application_ids(self):
        response = self.__fusionauth_client.retrieve_applications()
        assert response.was_successful() is True, \
            f'cannot retrieve applications'
        applications = response.success_response['applications']
        return [application['id'] for application in applications if application['name'] != 'FusionAuth']

    def get_application_id(self, app_name):
        response = self.__fusionauth_client.retrieve_applications()
        assert response.was_successful() is True, \
            f'cannot retrieve applications'
        applications = response.success_response['applications']
        application_ids_with_name = [application['id'] for application in applications if
                                     application['name'] == app_name]
        return application_ids_with_name[0] if len(application_ids_with_name) == 1 else None

    def get_roles_from_application_with_id(self, app_id):
        response = self.__fusionauth_client.retrieve_application(app_id)
        assert response.was_successful() is True, \
            f'cannot retrieve application with id {app_id}'
        application = response.success_response['application']
        # cannot be a set, this is a dict
        return application['roles']

    def get_roles_from_application_with_name(self, app_name):
        app_id = self.get_application_id(app_name)
        return self.get_roles_from_application_with_id(app_id)

    def applications_exist(self):
        app_ids = self.retrieve_application_ids()
        jwt_secret = self.get_hasura_graphql_jwt_secret()
        return len(app_ids) > 0 and len(jwt_secret['audience']) > 0 and len(
            self.get_role_names_from_user_management_actions()) > 0

    def no_application_exists(self):
        app_ids = self.retrieve_application_ids()
        jwt_secret = self.get_hasura_graphql_jwt_secret()
        return len(app_ids) == 0 and len(jwt_secret['audience']) == 0 and len(
            self.get_role_names_from_user_management_actions()) == 0

    def application_exists(self, app_name):
        app_id = self.get_application_id(app_name)
        jwt_secret = self.get_hasura_graphql_jwt_secret()
        all_role_names = self.get_role_names_from_user_management_actions()
        app_roles = self.get_roles_from_application_with_name(app_name)
        app_role_names = set(role['name'] for role in app_roles)
        return app_id is not None and app_id in jwt_secret['audience'] \
            and all_role_names.intersection(app_role_names) == app_role_names

    def create_application(self, app_name, role_names=None, app_id=None):
        if role_names is None:
            role_names = []
        env_name = self.__env_info.env_name()
        roles = ';'.join(role_names)
        success_text = self.__jps_client.install_from_file(self.__add_application_manifest_file, env_name, settings={
            'appName': app_name,
            'appRoles': roles,
            'almightyApiKey': self.__manifest_data['Auth Almighty API Key'],
            'appId': app_id
        })
        manifest_data = get_manifest_data(success_text)
        app_id = manifest_data['AppId']
        assert self.hasura_is_up()
        return app_id

    def delete_application(self, app_id):
        env_name = self.__env_info.env_name()
        self.__jps_client.install_from_file(self.__remove_application_manifest_file, env_name, settings={
            'appId': app_id,
            'almightyApiKey': self.__manifest_data['Auth Almighty API Key']
        })
        assert self.hasura_is_up()

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

    def get_hasura_graphql_jwt_secret(self):
        env_name = self.__env_info.env_name()
        env_vars = self.__control_client.get_container_env_vars_by_group(
            env_name, 'cp')
        jwt_secret = env_vars['HASURA_GRAPHQL_JWT_SECRET']
        return json.loads(jwt_secret)

    # TODO: here we should take all roles except "anonymous"
    def get_role_names_from_user_management_actions(self):
        env_name = self.__env_info.env_name()
        yaml_content = self.__file_client.read(
            env_name, '/hasura-metadata/actions.yaml', node_group='cp')
        yaml_data = yaml.load(yaml_content, yaml.Loader)
        actions = [action for action in yaml_data['actions']
                   if action['name'] != 'sign_in' and action['name'] != 'sign_up']
        role_names = set()
        for action in actions:
            if 'permissions' in action:
                for permission in action['permissions']:
                    role_names.add(permission['role'])
        return role_names

    def get_role_names_from_signin_action(self):
        env_name = self.__env_info.env_name()
        yaml_content = self.__file_client.read(
            env_name, '/hasura-metadata/actions.yaml', node_group='cp')
        yaml_data = yaml.load(yaml_content, yaml.Loader)
        actions = [action for action in yaml_data['actions']
                   if action['name'] == 'sign_in']
        role_names = set(
            permission['role'] for action in actions for permission in action['permissions'])
        return role_names

    # endregion

    # region GraphQL

    def get_emails(self):
        graphql_response = self.__execute_graphql_query(
            query_name='get_emails')
        assert 200 == graphql_response.status_code, \
            f'expected status code 200, got {graphql_response.status_code}'
        return graphql_response.data['data']

    def get_email_to_setup_password_for_user(self, username, timeout_in_sec=60, period_in_sec=1):
        def test_get_emails(developer):
            all_emails = developer.get_emails()['get_emails']['items']
            emails_to_setup_password = [
                email for email in all_emails
                if email['subject'] == 'Setup your password' and email['to'][0] == username]
            return 1 == len(emails_to_setup_password) > 0

        assert fail_after_timeout(
            lambda: test_get_emails(self), timeout_in_sec, period_in_sec) is True

        all_emails = self.get_emails()['get_emails']['items']
        emails_to_setup_password = [
            email for email in all_emails
            if email['subject'] == 'Setup your password' and email['to'] == username]
        return emails_to_setup_password[0]

    def __execute_graphql_query(self, query_name, variables=None):
        query = self.__get_query_from_file(query_name)
        graphql_response = self.__graphql_client.execute(
            query=query, variables=variables, auth_token=None, run_as_admin=True)
        return graphql_response

    def __get_query_from_file(self, query_name):
        path_to_query = os.path.join(
            self.__path_to_graphql_folder, f'{query_name}.graphql')
        with open(path_to_query, 'r') as file:
            return file.read().replace('\n', '')

    # endregion
