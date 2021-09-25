# TODO: install the database once and for all for the whole feature
Feature: The database

  The database holds the application state. Hasura bases on it
  to generate the graphql API.

  Background: sql node is available

    Given a jelastic environment with 2 postgres13 nodes is available in node group 'sqldb'
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
