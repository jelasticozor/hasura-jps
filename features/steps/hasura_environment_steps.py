import psycopg2
import requests
from behave import *

from features.utils.database import database_contains_table
from features.utils.faas import deploy, is_function_ready, faas_is_up
from features.utils.fusionauth import fusionauth_is_up
from features.utils.hasura import hasura_is_up


@when(u'a user creates table \'{table_name}\' on the {database} database')
def step_impl(context, table_name, database):
    database_connection = context.connections[database]
    cursor = database_connection.cursor()
    try:
        cursor.execute(
            f"""
            CREATE TABLE {table_name}(
                id int PRIMARY KEY NOT NULL
            );
            """
        )
        database_connection.commit()
    except psycopg2.errors.lookup('25006') as e:
        context.database_error = str(e)


@then(u'the postgres version is {postgres_version:d}')
def step_impl(context, postgres_version):
    min_version = postgres_version * 10000
    max_version = (postgres_version + 1) * 10000
    assert min_version <= context.connections['primary'].server_version < max_version
    assert min_version <= context.connections['secondary'].server_version < max_version


@then('she gets the error')
def step_impl(context):
    expected_error = context.text
    assert expected_error in context.database_error


@then('she sees table \'{table_name}\' in the {database} database')
def step_impl(context, table_name, database):
    database_connection = context.connections[database]
    assert database_contains_table(
        database_connection, table_name=table_name) is True


@then("fusionauth is available")
def step_impl(context):
    assert fusionauth_is_up(
        context.current_fusionauth_ip, context.fusionauth_port) is True


@then("the faas engine is available")
def step_impl(context):
    assert faas_is_up(context.faas_client) is True


@then("hasura is available")
def step_impl(context):
    assert hasura_is_up(
        context.hasura_node_ip, context.hasura_internal_port) is True


@then("the {function_name} function is ready")
def step_impl(context, function_name):
    assert is_function_ready(context.faas_client, function_name) is True


@then("the faas functions find the '{secret_content}' in the '{secret_name}'")
def step_impl(context, secret_name, secret_content):
    function_name = 'check-env'
    context.faas_client.login()
    deployment_success = deploy(
        context.faas_client, context.path_to_serverless_test_configuration, function_name)
    assert deployment_success is True

    rq = requests.post(
        f'http://{context.faas_client.endpoint}/function/{function_name}')
    assert rq.status_code == 200, f'expected status 200, got {rq.status_code}'
    secrets = rq.json()

    expected_secret = context.manifest_data[secret_content]
    assert expected_secret == secrets[
        secret_name], f'expected secret {expected_secret}, got {secrets[secret_name]}'


@then('the following extensions are installed on the {database_name} database')
def step_impl(context, database_name):
    expected_extensions = set(row['extension'] for row in context.table)
    cursor = context.connections[database_name].cursor()
    cursor.execute(
        """
        SELECT extname FROM pg_extension;
        """
    )
    fetched_rows = cursor.fetchall()
    actual_extensions = set(extension[0] for extension in fetched_rows)
    assert expected_extensions.intersection(
        actual_extensions) == expected_extensions


@then('the following schemas exist on the {database_name} database')
def step_impl(context, database_name):
    expected_schemas = set(row['schema'] for row in context.table)
    cursor = context.connections[database_name].cursor()
    cursor.execute(
        """
        SELECT schema_name FROM information_schema.schemata;
        """
    )
    fetched_rows = cursor.fetchall()
    actual_schemas = set(schema[0] for schema in fetched_rows)
    assert expected_schemas.intersection(actual_schemas) == expected_schemas


@then(u'there is {nb_nodes:d} {node_type} node in the {node_group} node group')
@then(u'there are {nb_nodes:d} {node_type} nodes in the {node_group} node group')
def step_impl(context, nb_nodes, node_type, node_group):
    node_ips = context.current_env_info.get_node_ips(
        node_group=node_group, node_type=node_type)
    assert len(node_ips) == nb_nodes
