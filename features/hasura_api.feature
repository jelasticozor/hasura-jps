# TODO: install the main manifest before the whole feature
Feature: Hasura API

  As a user,
  I want to use the hasura API,
  in order to build my system.

  Scenario: The faas engine is well-defined

    When a user installs the main manifest
    Then there is 1 docker node in the faas node group

  # TODO: check that there are two postgres nodes

  # TODO: check that we can log on hasura console as admin

  # TODO: try to log on as a user with some permissions and generate a jwt

  # TODO: test that hasura is still fine after node restart (e.g. access the /v1/version endpoint)

  # TODO: apply migrations that install a test API and validate
  #  - insertion to database
  #  - retrieval
  #  - eventing (call api endpoint which triggers an event which sets a value in the db; assert that the value has been set)
