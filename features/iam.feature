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
    Then she gets that the user was not found or the password was incorrect

  @fixture.api-user
  Scenario Outline: Sign in as registered user with one single role

    Given the api user has signed up on the application with role '<user role>'
    And she has received the email to set up her password
    And she has set her password
    When she signs in the application
    Then her JWT is valid
    And it contains the role '<user role>'

    Examples:
      | user role    |
      | default-role |
      | other-role   |

  @fixture.api-user
  Scenario Outline: Sign up with wrongly formatted email fails

    Given an api user with email '<email>'
    When she signs up on the application with role 'default-role'
    Then she gets the bad request error
    """
    Input email is not an email
    """

    Examples:
      | email        |
      | my-username  |
      | my-username@ |


  @fixture.api-user
  Scenario: Sign up with role that does not exist

    When the api user signs up on the application with role 'non-existent-role'
    Then she gets that it was not possible to sign her up

  # TODO: test 2 sign up with same user on same app with same role --> should fail

  # TODO: test 2 sign up with same user on same app with different roles --> should succeed, the function should grab the userId if it exists

  # TODO: test 2 set password with same changePasswordId --> should fail

  # TODO: sign up, set password, sign in, modify token, validate token ---> invalid token