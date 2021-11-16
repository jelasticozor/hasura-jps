from behave import *


@given("the user '{user_email}' registered on the test application")
def step_impl(context, user_email):
    response = context.fusionauth_client.retrieve_user_by_email(user_email)
    assert response.was_successful() is True, \
        f'cannot find user with email {user_email}'
    assert context.registered_user_on_test_application['username'] == user_email
    context.current_user_id = response['user']['id']
    app_id = context.auth_test_application
    response = context.fusionauth_client.retrieve_registration(
        context.current_user_id, app_id)
    assert response.was_successful() is True, \
        f'cannot find registration of user {context.current_user_id} on application {app_id}'


@when("she logs on with graphql mutation")
def step_impl(context):
    mutation = context.text
    response, _ = context.graphql_client.execute(
        query=mutation, variables={
            'username': context.registered_user_on_test_application['username'],
            'password': context.registered_user_on_test_application['password'],
            'appId': context.auth_test_application
        }, run_as_admin=False)
    assert 'errors' not in response
    context.current_jwt = response['data']['login']['token']


@then("her token validates by calling the following graphql mutation with bearer token")
def step_impl(context):
    mutation = context.text
    response, _ = context.graphql_client.execute(
        query=mutation, auth_token=context.current_jwt, run_as_admin=False)
    assert 'errors' not in response
    assert context.current_user_id == response['validate_token']['userId']
