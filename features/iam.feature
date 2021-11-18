Feature: Identity and Access Management

  As an API developer,
  I want to protect the relevant functionality
  with reliable identity and access management.

  Scenario: Login can be validated

    Given the user 'user@company.com' registered on the test application
    When she logs on with graphql mutation
    """
    mutation Login($username: String!, $password: String!, $appId: uuid!) {
      login(username: $username, password: $password, appId: $appId) {
        token
      }
    }
    """
    Then her token validates by calling the following graphql mutation with bearer token
    """
    mutation ValidateToken {
      validate_token {
        userId
      }
    }
    """