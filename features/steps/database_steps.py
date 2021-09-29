import os

import psycopg2
import psycopg2.errors
from test_utils.manifest_data import get_manifest_data

from features.utils.database import database_contains_table


@given(u'a jelastic environment with a postgres cluster')
def step_impl(context):
    path_to_manifest = os.path.join(
        context.test_manifests_folder, f'postgres-cluster.yml')
    success_text = context.jps_client.install_from_file(
        path_to_manifest,
        context.current_env_name)
    context.manifest_data = get_manifest_data(success_text)
    context.current_env_info = context.control_client.get_env_info(
        context.current_env_name)
    current_env_info = context.control_client.get_env_info(
        context.current_env_name)
    assert current_env_info.is_running()


@given(u'connections are established to the primary and secondary database nodes')
def step_impl(context):
    primary_node_ip = context.current_env_info.get_node_ip_from_name('Primary')
    assert primary_node_ip is not None
    secondary_node_ip = context.current_env_info.get_node_ip_from_name(
        'Secondary')
    assert secondary_node_ip is not None
    admin_user = context.manifest_data['Username']
    admin_password = context.manifest_data['Password']
    database_name = 'postgres'
    context.connections = {
        'primary': psycopg2.connect(
            host=primary_node_ip,
            user=admin_user,
            password=admin_password,
            database=database_name),
        'secondary': psycopg2.connect(
            host=secondary_node_ip,
            user=admin_user,
            password=admin_password,
            database=database_name)
    }


@when(u'a user creates a dummy table on the {database} database')
def step_impl(context, database):
    database_connection = context.connections[database]
    cursor = database_connection.cursor()
    try:
        cursor.execute(
            """
            CREATE TABLE dummy(
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


@then('she sees the dummy table in the {database} database')
def step_impl(context, database):
    database_connection = context.connections[database]
    assert database_contains_table(
        database_connection, table_name='dummy') is True
