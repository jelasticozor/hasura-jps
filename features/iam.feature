@fixture.jelastic-env
@fixture.api-developer
@fixture.api-user
Feature: Identity and Access Management

  As an API developer,
  I want to protect the relevant functionality
  with reliable identity and access management.

  Background: There exists an application

    Given an application named 'my-app' has been added with roles
      | role         |
      | default-role |
      | other-role   |

  Scenario: Sign in with invalid credentials

  The error codes provided by fusionauth are documented [here](https://fusionauth.io/docs/v1/tech/apis/login#authenticate-a-user).

    Given the api user has no account on the application
    When the api user signs in the application
    Then she gets an error that the user was not found or the password was incorrect

  @wip  
  Scenario Outline: Sign in as registered user with one single role

    Given the api user signed up on the application with role <user role>
    And she has received the email to setup her password
    # TODO: determine what permission should be set on the set_password mutation!
    And she set her password
    When she signs in the application
    Then her JWT is valid
    And it contains the role <user role>
    And she has a cookie with a refresh token

    Examples:
      | user role    |
      | default-role |
      | other-role   |