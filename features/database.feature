Feature: The database

  The database holds the application state.  
  Hasura bases on it to generate the graphql API.  
  Jelastic makes clusters of master-slave postgres  
  nodes available out-of-the-box.

  Background: Postgres cluster is available

    Given a jelastic environment with a postgres cluster
    And connections are established to the primary and secondary database nodes

  Scenario: Any change done on primary gets reflected on secondary

    When a user creates a dummy table on the primary database
    Then she sees the dummy table in the secondary database

  Scenario: Secondary is read-only

    When a user creates a dummy table on the secondary database
    Then she gets the error
    """
    cannot execute CREATE TABLE in a read-only transaction
    """

  Scenario: Postgres at least version 10 is installed

    Then the postgres version is 13
