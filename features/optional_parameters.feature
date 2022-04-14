@fixture.test-env-with-automatic-settings
@fixture.api-developer
Feature: Optional manifest parameters

  As an API developer,
  I might rely on optional parameters,
  in order to ease environment deployment.

  Scenario: Use automatic Jelastic user email as IAM admin email

    Then the 'Auth Admin Email' is the current Jelastic user email

  Scenario: Use automatic Hasura admin secret

    Then the 'Hasura Admin Secret' contains 40 characters