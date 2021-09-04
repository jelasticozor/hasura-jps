# TODO: install the database once and for all for the whole feature
Feature: The database

  The database holds the application state. Hasura bases on it
  to generate the graphql API.

  The requirements for hasura are documented [here](https://hasura.io/docs/latest/graphql/core/deployment/postgres-requirements.html).

  Background: sql node is available

    Given a jelastic environment with 2 postgres13 nodes is available in node group 'sqldb'
    And the database is installed

  @wip
  Scenario: Any change done on primary gets reflected on secondary

    When a user creates a dummy table on the primary database
    Then she sees the dummy table in the secondary database

  @wip
  Scenario: Secondary is read-only

    When a user creates a dummy table on the secondary database
    # TODO: tell exactly what error
    Then she gets an error

  @wip
  Scenario Outline: The necessary extensions are installed

    Then extension <extension> is installed

    Examples:

      | extension |
      | pgcrypto  |
      | citext    |
      | uuid-ossp |

  @wip
  Scenario Outline: Hasura-specific schemas are installed

    Then schema <schema> exists

    Examples:

      | schema      |
      | hdb_catalog |
      | hdb_views   |

  Scenario: At least version 10 is installed

    Then the postgres version is 13