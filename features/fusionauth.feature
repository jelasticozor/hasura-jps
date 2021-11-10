Feature: Fusionauth auth module

  Fusionauth is one of the possible Identity  
  and Authorization Management (IAM) modules.  
  It is used to generate JWTs that are  
  compatible with hasura.

  Scenario: Fusionauth is up and running

    Given a jelastic environment with a database and fusionauth
    When a user installs the fusionauth manifest
    Then fusionauth is up and running