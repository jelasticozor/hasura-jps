@fixture.test-env
@fixture.api-developer
Feature: Identity and Access Management

  As an API developer,
  I want to protect the relevant functionality
  with reliable identity and access management.

  Background: There exists an application

    Given an application named 'my-app' has been added with roles
      | role         |
      | default-role |
      | other-role   |

  @fixture.api-user
  Scenario: Valid access token can be refreshed with valid refresh token

    The access token is refreshed upon calling the jwt refresh query. The
    refresh token is not refreshed, because it is not a one-time use token,
    as implemented [here](https://gitlab.hidora.com/softozor/hasura-jps/-/blob/master/fusionauth/create_application.py#L37).
    Instead, it has a token time to live in minutes, and as long as this time
    has not gone by, the refresh token will remain the same.

    Given the api user has a valid account on the application with role 'default-role'
    And she has signed in
    When she refreshes her access token with her valid refresh token
    Then she gets a new access token
    But the same refresh token

  @fixture.api-user
  Scenario: Valid access token cannot be refreshed with invalid refresh token

    Given the api user has a valid account on the application with role 'default-role'
    And she has signed in
    When she refreshes her access token with an invalid refresh token
    Then she gets notified with the bad request error
    """
    Unable to refresh JWT
    """

  @fixture.api-user
  Scenario: Invalid access token cannot be refreshed with valid refresh token

    Given the api user has a valid account on the application with role 'default-role'
    And she has signed in
    When she refreshes an invalid access token with her valid refresh token
    Then she gets notified of the access token invalidity


  @fixture.api-user
  Scenario: Sign in with invalid credentials

  The error codes provided by fusionauth are documented [here](https://fusionauth.io/docs/v1/tech/apis/login#authenticate-a-user).

    Given the api user has no account on the application
    When she signs in
    Then she gets notified that the user was not found or the password was incorrect

  @fixture.api-user
  Scenario Outline: Sign in as registered user with one single role

    Given the api user has signed up on the application with role '<user role>'
    And she has received the email to set up her password with a one-time token
    And she has set her password with that token
    When she signs in
    Then her access token is valid
    And it contains the role '<user role>'

    Examples:
      | user role    |
      | default-role |
      | other-role   |

  @fixture.api-user
  Scenario: Sign in as registered user with multiple roles

    Given the api user has signed up on the application with all available roles
    And she has received the email to set up her password with a one-time token
    And she has set her password with that token
    When she signs in
    Then her access token is valid
    And it contains all the roles in the application

  @fixture.api-user
  Scenario Outline: Sign up with wrongly formatted email fails

    Given an api user with email '<email>'
    When she signs up on the application with role 'default-role'
    Then she gets notified with the bad request error
    """
    Input email is not an email
    """

    Examples:
      | email        |
      | my-username  |
      | my-username@ |
      | domain.com   |
      | @domain.com  |

  @fixture.api-user
  Scenario: Sign up with role that does not exist

    When the api user signs up on the application with role 'non-existent-role'
    Then she gets notified with a bad request error

  @fixture.api-user
  Scenario: The token to set the password is a one-time token

    Given the api user has signed up on the application with role 'default-role'
    And she has received the email to set up her password with a one-time token
    And she has set her password with that token
    When she sets her password with that token again
    Then she gets notified that the user was not found

  @fixture.api-user
  Scenario: Sign up twice with same role

    Given the api user has signed up on the application with role 'default-role'
    When she signs up on the application with role 'default-role'
    Then she gets notified with a bad request error  

  @fixture.api-user
  Scenario: Sign up twice with different roles

    Given the api user has signed up on the application with role 'default-role'
    And she has received the email to set up her password with a one-time token
    And she has set her password with that token
    When she signs up on the application with role 'other-role'
    Then she gets notified with a bad request error
