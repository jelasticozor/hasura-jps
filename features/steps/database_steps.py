import psycopg2
import psycopg2.errors
from behave import *

from features.utils.database import database_contains_table


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
