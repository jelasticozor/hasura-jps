# TODO: install the main manifest before the whole feature
Feature: All together

  As a user,
  I want to use the system as a whole,
  in order to have a working graphql API at hand.

  Scenario: The faas engine is well-defined

    When a user installs the main manifest
    Then there is 1 docker node in the faas node group

  # TODO: check that there are two postgres nodes

  # TODO: check that we can log on hasura console as admin

  # TODO: try to log on as a user with some permissions and generate a jwt