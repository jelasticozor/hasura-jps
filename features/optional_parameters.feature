Feature: Optional manifest parameters

  As an API developer,
  I might rely on optional parameters,
  in order to ease environment deployment.

  @fixture.jelastic-env-with-automatic-auth-admin-email
  Scenario: Use automatic Jelastic user email as IAM admin email

    Then the 'Auth Admin Email' is the current Jelastic user email

  @fixture.jelastic-env-with-automatic-hasura-admin-secret
  Scenario: Use automatic Hasura admin secret

    Then the 'Hasura Admin Secret' contains 40 characters