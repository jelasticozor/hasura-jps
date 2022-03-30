from behave import *


@given("the api user has no account on the application")
def step_impl(context):
    assert context.api_user.user_id is None


@given("the api user signed up on the application with role {role}")
def step_impl(context, role):
    graphql_response = context.api_user.sign_up(
        role, context.current_app_id)
    assert 200 == graphql_response.status_code, \
        f'expected status code 200, got {graphql_response.status_code}'
    assert 'errors' not in graphql_response.data, \
        f'expected no error in graphql response, got {graphql_response.data}'
    assert context.api_user.user_id is not None


@given("she set her password")
def step_impl(context):
    graphql_response = context.api_user.set_password(
        context.current_change_password_id)
    assert 200 == graphql_response.status_code, \
        f'expected status code 200, got {graphql_response.status_code}'


@when("the api user signs in the application")
@when("she signs in the application")
def step_impl(context):
    context.current_graphql_response = context.api_user.sign_in(
        context.current_app_id)


@then("she gets an error that the user was not found or the password was incorrect")
def step_impl(context):
    actual_status_code = context.current_graphql_response.status_code
    assert actual_status_code is 404, \
        f'expected status code 404, got {actual_status_code}'
    actual_data = context.current_graphql_response.data
    assert 'errors' in actual_data, \
        f'expected errors in graphql response, got none: {actual_data}'


@then("her JWT is valid")
def step_impl(context):
    graphql_response = context.api_user.validate_token()
    assert 200 == graphql_response.status_code, \
        f'expected status code 200, got {graphql_response.status_code}'


@then("she has a cookie with a refresh token")
def step_impl(context):
    assert 'refresh-token' in context.current_graphql_response.cookies, \
        f'expected refresh-token key in cookies, got {context.current_graphql_response.cookies}'
