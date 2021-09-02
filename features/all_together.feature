Feature: All together

  As a user,
  I want to use the system as a whole,
  in order to have a working graphql API at hand.

  Scenario: The faas engine is well-defined

    When a user installs the main manifest
    Then there is 1 single docker node in the faas node group
