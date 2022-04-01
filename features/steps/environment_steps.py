import psycopg2
from behave import *


@when('the api developer creates table \'{table_name}\' on the {database} database')
def step_impl(context, table_name, database):
    try:
        context.api_developer.create_table_in_database(
            table_name, database)
    except psycopg2.errors.lookup('25006') as e:
        context.database_error = str(e)


@then('the database has postgres version {postgres_version:d}')
def step_impl(context, postgres_version):
    min_version = postgres_version * 10000
    max_version = (postgres_version + 1) * 10000
    assert min_version <= context.api_developer.get_database_version(
        'primary') < max_version
    assert min_version <= context.api_developer.get_database_version(
        'secondary') < max_version


@then('she gets the error')
def step_impl(context):
    expected_error = context.text
    assert expected_error in context.database_error


@then('she sees table \'{table_name}\' in the {database} database')
def step_impl(context, table_name, database):
    assert context.api_developer.database_contains_table(
        database, table_name) is True


@then('the iam engine is up')
def step_impl(context):
    assert context.api_developer.fusionauth_is_up() is True


@then('the faas engine is up')
def step_impl(context):
    assert context.api_developer.faas_is_up() is True


@then('hasura is up')
def step_impl(context):
    assert context.api_developer.hasura_is_up() is True


@then('the {function_name} function is ready')
def step_impl(context, function_name):
    assert context.api_developer.is_function_ready(function_name) is True


@then('the faas functions find the \'{secret_content}\' in the \'{secret_name}\'')
def step_impl(context, secret_content, secret_name):
    function_name = 'check-env'
    context.api_developer.log_on_faas()
    deployment_success = context.api_developer.deploy_function(
        context.path_to_serverless_test_configuration, function_name)
    assert deployment_success is True
    secrets = context.api_developer.invoke_function(function_name)
    expected_secret = context.manifest_data[secret_content]
    assert expected_secret == secrets[
        secret_name], f'expected secret {expected_secret}, got {secrets[secret_name]}'


@then('the following extensions are installed on the {database_name} database')
def step_impl(context, database_name):
    expected_extensions = set(row['extension'] for row in context.table)
    actual_extensions = context.api_developer.get_database_extensions(
        database_name)
    assert expected_extensions.intersection(
        actual_extensions) == expected_extensions


@then('the following schemas exist on the {database_name} database')
def step_impl(context, database_name):
    expected_schemas = set(row['schema'] for row in context.table)
    actual_schemas = context.api_developer.get_database_schemas(database_name)
    assert expected_schemas.intersection(actual_schemas) == expected_schemas


@step("the test mail server is up")
def step_impl(context):
    assert context.api_developer.mailhog_is_up() is True
