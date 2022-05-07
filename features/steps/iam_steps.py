import re

import jwt
from behave import *


@given("application '{app_name}' with roles")
def step_impl(context, app_name):
    expected_app_id = context.api_developer.get_application_id(app_name)
    assert expected_app_id == context.current_app_id, \
        f'expected application id {expected_app_id}, got {context.current_app_id}'
    context.expected_role_names = [row['role'] for row in context.table]
    actual_roles = context.api_developer.get_roles_from_application_with_name(
        app_name)
    actual_role_names = [role['name'] for role in actual_roles]
    assert set(context.expected_role_names) == set(actual_role_names), \
        f'expected {set(context.expected_role_names)}, got {set(actual_role_names)}'


@given("the api user has no account on the application")
def step_impl(context):
    assert context.api_user.user_id is None


@given("the api user has signed up on the application with role '{role}'")
def the_api_user_has_signed_up_on_the_application_with_role(context, role):
    graphql_response = context.api_user.sign_up(
        [role], context.current_app_id)
    assert 'errors' not in graphql_response.payload, \
        f'expected no error, got {graphql_response.payload}'
    assert context.api_user.user_id is not None


@given("the api user has signed up on the application with all available roles")
def step_impl(context):
    graphql_response = context.api_user.sign_up(
        context.expected_role_names, context.current_app_id)
    assert 'errors' not in graphql_response.payload, \
        f'expected no error, got {graphql_response.payload}'
    assert context.api_user.user_id is not None


@given("she has set her password with that token")
def she_has_set_her_password_with_that_token(context):
    graphql_response = context.api_user.set_password(
        context.current_change_password_id)
    assert 'errors' not in graphql_response.payload, \
        f'expected no error, got {graphql_response.payload}'


@given("she has received the email to set up her password with a one-time token")
def she_has_received_the_email_to_set_up_her_password_with_a_one_time_token(context):
    email = context.api_developer.read_and_forget_email_to_setup_password_for_user(
        context.api_user.username)
    assert email is not None, \
        f'expected email, got None'
    email_body = email['body']
    match = re.search('<p>changePasswordId=(.+)</p>', email_body)
    assert match, \
        f'expected to find changePasswordId in email body {email_body}'
    context.current_change_password_id = match.group(1)


@given("an api user with email '{email}'")
def step_impl(context, email):
    context.api_user.username = email


@given("the api user has a valid account on the application with role '{role}'")
def step_impl(context, role):
    the_api_user_has_signed_up_on_the_application_with_role(context, role)
    she_has_received_the_email_to_set_up_her_password_with_a_one_time_token(
        context)
    she_has_set_her_password_with_that_token(context)


@given("she has signed in")
def step_impl(context):
    graphql_response = context.api_user.sign_in(
        context.current_app_id)
    assert 'errors' not in graphql_response.payload, \
        f'expected no error, got {graphql_response.payload}'
    payload = graphql_response.payload['data']['sign_in']
    context.original_access_token = payload['token']
    context.original_refresh_token = payload['refresh_token']


@when("she signs in")
def step_impl(context):
    context.current_graphql_response = context.api_user.sign_in(
        context.current_app_id)


@when("the api user signs up on the application with role '{role}'")
@when("she signs up on the application with role '{role}'")
def step_impl(context, role):
    context.current_graphql_response = context.api_user.sign_up(
        [role], context.current_app_id)


@when("she sets her password with that token again")
def step_impl(context):
    context.current_graphql_response = context.api_user.set_password(
        context.current_change_password_id)


@when("she refreshes her access token with her valid refresh token")
def step_impl(context):
    context.current_graphql_response = context.api_user.refresh_jwt()


@when("she refreshes her access token with an invalid refresh token")
def step_impl(context):
    context.api_user.refresh_token = 'invalid-refresh-token'
    context.current_graphql_response = context.api_user.refresh_jwt()


@when("she refreshes an invalid access token with her valid refresh token")
def step_impl(context):
    context.api_user.jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVKUDNLOXFiRTFVb3RfQWdla3paOTVyWFR3OCJ9.eyJhdWQiOiJiNTUxODRlZi1mZDViLTQxMjktOGI5MC03MDgyZTRlNDZlZDEiLCJleHAiOjE2NDg2NzMzOTMsImlhdCI6MTY0ODY2OTc5MywiaXNzIjoieW91ci1jb21wYW55LmNvbSIsInN1YiI6IjM3NzI5NzQ0LTliNTUtNGE4Ni05MGM1LWYyZjlhYTkwZTAxYyIsImp0aSI6IjAyNTQ2Mzk3LTA0ZmEtNDM0YS05NTcyLTNiZDlkODEyMTQyNCIsImF1dGhlbnRpY2F0aW9uVHlwZSI6IlBBU1NXT1JEIiwiZW1haWwiOiJ6YWRpZ3VzQGhvdG1haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImFwcGxpY2F0aW9uSWQiOiJiNTUxODRlZi1mZDViLTQxMjktOGI5MC03MDgyZTRlNDZlZDEiLCJyb2xlcyI6WyJkZWZhdWx0LXJvbGUiXSwiaHR0cHM6Ly9oYXN1cmEuaW8vand0L2NsYWltcyI6eyJ4LWhhc3VyYS1hbGxvd2VkLXJvbGVzIjpbImRlZmF1bHQtcm9sZSJdLCJ4LWhhc3VyYS1kZWZhdWx0LXJvbGUiOiJkZWZhdWx0LXJvbGUiLCJ4LWhhc3VyYS11c2VyLWlkIjoiMzc3Mjk3NDQtOWI1NS00YTg2LTkwYzUtZjJmOWFhOTBlMDFjIn19.k6tbJboQNSuL7IXnqE9dH_K5027zd8Jcqd36VoQos3qVy5gJhSS1oz2guEiFHAN_zu3mTufx__wl8ogd64JFnv1-47YyNUYnhiuLCULeyFz1cMEVSu0K-cW0fiCIFCWEcFbZG62DFENWbLq4Khp-XeTqCdzierW3YBh-1Ld5i8ovfk1_X3wgdle7XAk8XDQmlLJxbEMjjOpfhsbUkfHs9L2oM2lsPhDCrQQO3qh4mIfcXNbJhclMu9XrT-RR_iDmE27FetfW86R3zGYX1ly0HOZ7jAwjzeA_miuKlT9eqSjyHugH0jagwPiDXX-FbmLVAtD3kLgRn4CnSfM_7SbTaA'
    context.current_graphql_response = context.api_user.refresh_jwt()


@then("she gets notified that the user was not found")
@then("she gets notified that the user was not found or the password was incorrect")
def step_impl(context):
    payload = context.current_graphql_response.payload
    assert 'errors' in payload, \
        f'expected errors in graphql response, got none: {payload}'
    actual_status_code = int(payload['errors'][0]['extensions']['code'])
    assert 404 == actual_status_code, \
        f'expected status code 404, got {actual_status_code}'


@then("her access token is valid")
def step_impl(context):
    graphql_response = context.api_user.validate_token()
    assert 'errors' not in graphql_response.payload, \
        f'expected no error, got {graphql_response.payload}'


@then("it contains the role '{role}'")
def step_impl(context, role):
    # sample token:
    # eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVKUDNLOXFiRTFVb3RfQWdla3paOTVyWFR3OCJ9.eyJhdWQiOiJiNTUxODRlZi1mZDViLTQxMjktOGI5MC03MDgyZTRlNDZlZDEiLCJleHAiOjE2NDg2NzMzOTMsImlhdCI6MTY0ODY2OTc5MywiaXNzIjoieW91ci1jb21wYW55LmNvbSIsInN1YiI6IjM3NzI5NzQ0LTliNTUtNGE4Ni05MGM1LWYyZjlhYTkwZTAxYyIsImp0aSI6IjAyNTQ2Mzk3LTA0ZmEtNDM0YS05NTcyLTNiZDlkODEyMTQyNCIsImF1dGhlbnRpY2F0aW9uVHlwZSI6IlBBU1NXT1JEIiwiZW1haWwiOiJ6YWRpZ3VzQGhvdG1haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImFwcGxpY2F0aW9uSWQiOiJiNTUxODRlZi1mZDViLTQxMjktOGI5MC03MDgyZTRlNDZlZDEiLCJyb2xlcyI6WyJkZWZhdWx0LXJvbGUiXSwiaHR0cHM6Ly9oYXN1cmEuaW8vand0L2NsYWltcyI6eyJ4LWhhc3VyYS1hbGxvd2VkLXJvbGVzIjpbImRlZmF1bHQtcm9sZSJdLCJ4LWhhc3VyYS1kZWZhdWx0LXJvbGUiOiJkZWZhdWx0LXJvbGUiLCJ4LWhhc3VyYS11c2VyLWlkIjoiMzc3Mjk3NDQtOWI1NS00YTg2LTkwYzUtZjJmOWFhOTBlMDFjIn19.k6tbJboQNSuL7IXnqE9dH_K5027zd8Jcqd36VoQos3qVy5gJhSS1oz2guEiFHAN_zu3mTufx__wl8ogd64JFnv1-47YyNUYnhiuLCULeyFz1cMEVSu0K-cW0fiCIFCWEcFbZG62DFENWbLq4Khp-XeTqCdzierW3YBh-1Ld5i8ovfk1_X3wgdle7XAk8XDQmlLJxbEMjjOpfhsbUkfHs9L2oM2lsPhDCrQQO3qh4mIfcXNbJhclMu9XrT-RR_iDmE27FetfW86R3zGYX1ly0HOZ7jAwjzeA_miuKlT9eqSjyHugH0jagwPiDXX-FbmLVAtD3kLgRn4CnSfM_7SbTaA
    # corresponds to
    # {
    #     "aud": "b55184ef-fd5b-4129-8b90-7082e4e46ed1",
    #     "exp": 1648673393,
    #     "iat": 1648669793,
    #     "iss": "your-company.com",
    #     "sub": "37729744-9b55-4a86-90c5-f2f9aa90e01c",
    #     "jti": "02546397-04fa-434a-9572-3bd9d8121424",
    #     "authenticationType": "PASSWORD",
    #     "email": "zadigus@hotmail.com",
    #     "email_verified": true,
    #     "applicationId": "b55184ef-fd5b-4129-8b90-7082e4e46ed1",
    #     "roles": [
    #         "default-role"
    #     ],
    #     "https://hasura.io/jwt/claims": {
    #         "x-hasura-allowed-roles": [
    #             "default-role"
    #         ],
    #         "x-hasura-default-role": "default-role",
    #         "x-hasura-user-id": "37729744-9b55-4a86-90c5-f2f9aa90e01c"
    #     }
    # }
    decoded_jwt = jwt.decode(context.api_user.jwt, options={
        "verify_signature": False})
    assert role in decoded_jwt['roles'], \
        f'expected {decoded_jwt} to contain role {role}'
    assert role in decoded_jwt['https://hasura.io/jwt/claims']['x-hasura-allowed-roles'], \
        f'expected {decoded_jwt} to contain role {role}'


@then("it contains all the roles in the application")
def step_impl(context):
    decoded_jwt = jwt.decode(context.api_user.jwt, options={
        "verify_signature": False})
    actual_role_names = set(decoded_jwt['roles'])
    expected_role_names = set(context.expected_role_names)
    assert expected_role_names == actual_role_names, \
        f'expected {decoded_jwt} to contain all roles {expected_role_names}, got {actual_role_names} instead'


@then("she gets notified with the bad request error")
def step_impl(context):
    payload = context.current_graphql_response.payload
    assert 'errors' in payload, \
        f'expected errors in graphql response, got none: {payload}'
    actual_status_code = int(payload['errors'][0]['extensions']['code'])
    assert 400 == actual_status_code, \
        f'expected status code 400, got {actual_status_code}'
    expected_error = context.text
    assert expected_error == payload['errors'][0]['message'], \
        f'expected error {expected_error}, got {payload["errors"][0]["message"]}'


@then("she gets notified with a bad request error")
def step_impl(context):
    payload = context.current_graphql_response.payload
    assert 'errors' in payload, \
        f'expected errors in graphql response, got none: {payload}'
    actual_status_code = int(payload['errors'][0]['extensions']['code'])
    assert 400 == actual_status_code, \
        f'expected status code 400, got {actual_status_code}'


@then("she gets a new access token")
def step_impl(context):
    payload = context.current_graphql_response.payload
    assert 'errors' not in payload, \
        f'expected no error, got {payload}'
    refresh_jwt_payload = payload['data']['refresh_jwt']
    assert context.original_access_token != refresh_jwt_payload['token'], \
        f'expected original access token {context.original_access_token} to be different from new access token {refresh_jwt_payload["token"]}'


@then("the same refresh token")
def step_impl(context):
    payload = context.current_graphql_response.payload
    assert 'errors' not in payload, \
        f'expected no error, got {payload}'
    refresh_jwt_payload = payload['data']['refresh_jwt']
    assert context.original_refresh_token == refresh_jwt_payload['refresh_token'], \
        f'expected new refresh token {refresh_jwt_payload["refresh_token"]} to be the same as the original {context.original_refresh_token}'


@then("she gets notified of the access token invalidity")
def step_impl(context):
    payload = context.current_graphql_response.payload
    assert 'errors' in payload, \
        f'expected errors in graphql response, got none: {payload}'
    actual_error_code = payload['errors'][0]['extensions']['code']
    assert 'invalid-jwt' == actual_error_code, \
        f'expected error code to be \'invalid-jwt\', got \'{actual_error_code}\''
