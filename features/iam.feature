@fixture.jelastic-env
@fixture.api-developer
@fixture.auth-test-application
@fixture.registered-user-on-test-application
Feature: Identity and Access Management

  As an API developer,
  I want to protect the relevant functionality
  with reliable identity and access management.

  Scenario: Signin can be validated

    Given the user 'user@company.com' registered on the test application
    When she logs on with graphql mutation
    """
    query SignIn($username: String!, $password: String!, $appId: uuid!) {
      sign_in(username: $username, password: $password, app_id: $appId) {
        token
      }
    }
    """
    Then her token validates by calling the following graphql mutation with bearer token
    """
    query ValidateToken {
      validate_token {
        user_id
      }
    }
    """
