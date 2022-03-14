@fixture.jelastic-env
@fixture.api-developer
Feature: Create applications

  As an API developer,  
  I want to create new applications,  
  so that clients can identify.

  An application is something a user can log into.
  It is characterized by an application id.

  Application creation is made available through Jelastic
  manifest [add_application](https://gitlab.hidora.com/softozor/hasura-jps/-/raw/master/add-application.yml).
  Its counterpart Jelastic manifest [remove_application](https://gitlab.hidora.com/softozor/hasura-jps/-/raw/master/remove-application.yml)
  allows to remove an application.

  Background: No application exists

    Given no application exists

  @fixture.remove-applications
  Scenario: The application id is automatically generated

    When the api developer adds application 'app-1' with roles
      | role  |
      | role1 |
      | role2 |
      | role3 |
    Then its application id is generated automatically
    And application 'app-1' is associated with that id on the iam service
    And that application id is listed in the hasura jwt audience
    And the roles are defined on the application
    And 'role1' is the default role
    And the roles are granted permission to execute all user management actions except 'login'

  @fixture.remove-applications
  Scenario: The api developer provides the application id

  An application id is a version 4 uuid.

    When the api developer adds application 'app-1' with id '2b083796-1afb-4c3a-8866-5e83cc469bb6' and roles
      | role  |
      | role1 |
      | role2 |
      | role3 |
    Then application 'app-1' is associated with that id on the iam service
    And that application id is listed in the hasura jwt audience
    And the roles are defined on the application
    And 'role1' is the default role
    And the roles are granted permission to execute all user management actions except 'login'

  @fixture.remove-applications
  Scenario: The api developer adds two applications

    Given an application named 'app-1' has been added with roles
      | role  |
      | role1 |
      | role2 |
      | role3 |
    When the api developer adds application 'app-2' with roles
      | role  |
      | role2 |
      | role4 |
    Then application 'app-2' exists
    And its application id is listed in the hasura jwt audience
    And the roles are granted permission to execute all user management actions except 'login'