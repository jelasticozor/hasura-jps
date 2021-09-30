Feature: Fusionauth auth module

  Fusionauth is one of the possible Identity
  and Authorization Management (IAM) modules.
  In essence, it generates JWTs that are
  compatible with hasura.

  Background: Jelastic environment ready

    Given a jelastic environment with a database and fusionauth

  @current  
  Scenario: Fusionauth works without kick-starting

    When a user installs the fusionauth manifest without kick-starting
    Then fusionauth is up and running

  Scenario: Fusionauth works with kick-starting

    When a user installs the fusionauth manifest with kick-starting
    Then fusionauth is up and running