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
    Then her JWT is valid
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
    Then her JWT is valid
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
  Scenario: Sign up with role that does not exist

    Given the api user has signed up on the application with role 'default-role'
    When she signs up on the application with role 'default-role'
    Then she gets notified with a bad request error

  @fixture.api-user
  Scenario: The token to set the password is a one-time token

    Given the api user has signed up on the application with role 'default-role'
    And she has received the email to set up her password with a one-time token
    And she has set her password with that token
    When she sets her password with that token again
    Then she gets notified that the user was not found

  # TODO: test 2 sign up with same user on same app with different roles
  #   --> should succeed, the function should grab the userId if it exists
  #   --> should not send set password email