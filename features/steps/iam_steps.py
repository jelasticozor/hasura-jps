from behave import *


@given('the user \'{user_email}\' registered on the test application')
def step_impl(context, user_email):
    assert context.registered_user_on_test_application['email'] == user_email
    context.current_user_id = context.api_developer.retrieve_user_by_email(user_email)[
        'id']
    app_id = context.auth_test_application
    context.api_developer.check_user_is_registered_on_application(
        context.current_user_id, app_id)


@when('she logs on with graphql mutation')
def step_impl(context):
    mutation = context.text
    response = context.api_developer.post_graphql(
        query=mutation,
        variables={
            'username': context.registered_user_on_test_application['email'],
            'password': context.registered_user_on_test_application['password'],
            'appId': context.auth_test_application
        },
        run_as_admin=False)
    context.current_jwt = response['login']['token']


@then('her token validates by calling the following graphql mutation with bearer token')
def step_impl(context):
    mutation = context.text
    response = context.api_developer.post_graphql(
        query=mutation,
        auth_token=context.current_jwt,
        run_as_admin=False
    )
    assert context.current_user_id == response['validate_token']['userId']
