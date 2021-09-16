# TODO: install the main manifest before the whole feature
Feature: Hasura API

  As a user,
  I want to use the hasura API,
  in order to build my system.

  Background: The main manifest is installed

    Given the user has installed the main manifest

  Scenario: The faas engine is well-defined

    Then there is 1 docker node in the faas node group

  Scenario: The database is deployed in a master-slave architecture

    Then there are 2 postgres13 nodes in the sqldb node group  

  Scenario: The api is deployed in the cp node group

    Then there is 1 docker node in the cp node group

  # TODO: check that we have the nginx node installed

  # TODO: check that the nginx has ssl installed

  # TODO: check that we can log on hasura console as admin
  #  - log on doesn't exist
  #  - can I apply the migrations without the admin-secret? if not, then hasura migrate apply will be the check that it works

  # TODO: test that hasura is still fine after node restart (e.g. access the /v1/version endpoint)

  # TODO: apply migrations that install a test API and validate
  #  - insertion to database
  #  - retrieval
  #  - eventing (call api endpoint which triggers an event which sets a value in the db; assert that the value has been set)

  # TODO: try to log on as a user with some permissions and generate a jwt
