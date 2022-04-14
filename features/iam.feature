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
    When she signs in the application
    Then she gets an error that the user was not found or the password was incorrect

  @fixture.api-user
  Scenario Outline: Sign in as registered user with one single role

    Given the api user has signed up on the application with role <user role>
    And she has received the email to set up her password
    And she has set her password
    When she signs in the application
    Then her JWT is valid
    And it contains the role '<user role>'
    # TODO: this does not seem to be supported by hasura --> give the refresh token in the graphql response body
    # And she has a cookie with a refresh token

    Examples:
      | user role    |
      | default-role |
      | other-role   |

  # TODO: test with email argument that is not an email --> should fail

  # TODO: test 1 sign up with role that does not exist on application --> should fail

  # TODO: test 2 sign up with same user on same app with same role --> should fail

  # TODO: test 2 sign up with same user on same app with different roles --> should succeed, the function should grab the userId if it exists

  # TODO: test 2 set password with same changePasswordId --> should fail

  # TODO: sign up, set password, sign in, modify token, validate token ---> invalid token