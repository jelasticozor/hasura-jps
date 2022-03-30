from uuid import UUID

from behave import *


@given("no application exists")
def step_impl(context):
    assert context.api_developer.no_application_exists()


@given("an application named '{app_name}' has been added with roles")
@when("the api developer adds application '{app_name}' with roles")
def step_impl(context, app_name):
    context.expected_role_names = [row['role'] for row in context.table]
    context.current_app_id = context.api_developer.create_application(
        app_name, context.expected_role_names)
    context.app_ids.append(context.current_app_id)


@when("the api developer adds application '{app_name}' with id '{app_id}' and roles")
def step_impl(context, app_name, app_id):
    context.expected_role_names = [row['role'] for row in context.table]
    context.current_app_id = context.api_developer.create_application(
        app_name, context.expected_role_names, app_id=app_id)
    assert app_id == context.current_app_id, \
        f'expected application id {app_id}, got {context.current_app_id}'
    context.app_ids.append(context.current_app_id)


def is_uuid4(app_id):
    try:
        uuid = UUID(app_id, version=4)
        return str(uuid) == app_id
    except ValueError:
        return False


@then("its application id is generated automatically")
def step_impl(context):
    assert is_uuid4(context.current_app_id), \
        f'expected {context.current_app_id} to be a version 4 uuid'


@then("application '{app_name}' is associated with that id on the iam service")
def step_impl(context, app_name):
    app_id = context.api_developer.get_application_id(app_name)
    assert context.current_app_id == app_id, \
        f'expected application id {context.current_app_id} to be associated with application name {app_name}, got {app_id}'


@then("its application id is listed in the hasura jwt audience")
@then("that application id is listed in the hasura jwt audience")
def step_impl(context):
    jwt_secret = context.api_developer.get_hasura_graphql_jwt_secret()
    jwt_audience = jwt_secret['audience']
    assert context.current_app_id in jwt_audience, \
        f'expected {context.current_app_id} to be contained in {jwt_audience}'


@then("the roles are defined on the application")
def step_impl(context):
    actual_application_roles = context.api_developer.get_roles_from_application_with_id(
        context.current_app_id)
    actual_application_role_names = [role['name']
                                     for role in actual_application_roles]
    assert set(context.expected_role_names) == set(actual_application_role_names), \
        f'expected {set(context.expected_role_names)}, got {set(actual_application_role_names)}'


@then("application '{app_name}' exists")
def step_impl(context, app_name):
    assert context.api_developer.application_exists(app_name), \
        f'expected application {app_name} to exist'


@then("'{role_name}' is the default role")
def step_impl(context, role_name):
    actual_application_roles = context.api_developer.get_roles_from_application_with_id(
        context.current_app_id)
    actual_default_application_role_names = [
        role['name'] for role in actual_application_roles if role['isDefault']]
    assert len(actual_default_application_role_names) == 1, \
        f'expected one single default application role name, got {actual_default_application_role_names}'
    actual_default_application_role_name = actual_default_application_role_names[0]
    assert role_name == actual_default_application_role_name, \
        f'expected default role name {context.expected_role_names[0]}, got {actual_default_application_role_name}'


@then("the roles are granted permission to execute all user management actions except 'sign_in'")
def step_impl(context):
    actual_user_mgmt_actions_role_names = context.api_developer.get_role_names_from_user_management_actions()
    expected_role_names = set(context.expected_role_names)
    assert expected_role_names == expected_role_names.intersection(actual_user_mgmt_actions_role_names), \
        f'expected {expected_role_names} to be contained in {actual_user_mgmt_actions_role_names}'
    actual_login_action_role_names = context.api_developer.get_role_names_from_signin_action()
    assert len(expected_role_names.intersection(actual_login_action_role_names)) == 0, \
        f'expected {expected_role_names} not to be contained in {actual_login_action_role_names}'
