@development
@fixture.test-env
@fixture.api-developer
Feature: Development Hasura environment

  As an API developer,  
  I want a hasura environment optimized for development,  
  so that I can test and monitor my API developments.

  The requirements for hasura are documented [here](https://hasura.io/docs/latest/graphql/core/deployment/postgres-requirements.html).

  Scenario: The Jelastic environment is well-defined

    Then the iam engine is up
    And the faas engine is up
    And hasura is up
    And the database has postgres version 13
    And the test mail server is up

  Scenario: The IAM functions are well-defined

    Then the sign-in function is ready
    And the validate-token function is ready 
    And the sign-up function is ready
    And the set-password function is ready 
    And the refresh-jwt function is ready
    And the get-emails function is ready
    And the delete-all-emails function is ready
    And the delete-email function is ready
    And the faas functions find the 'Auth Serverless API Key' in the 'auth-secret'

  Scenario: The database meets the relevant preconditions

  The only extension required by hasura is [pgcrypto](https://www.postgresql.org/docs/13/pgcrypto.html).
  The [citext extension](https://www.postgresql.org/docs/13/citext.html) provides case-insensitive character
  string type and the [uuid-ossp extension](https://www.postgresql.org/docs/13/uuid-ossp.html) provides functions
  to generate UUIDs.

    Then the following extensions are installed on the hasura database
      | extension |
      | pgcrypto  |
      | citext    |
      | uuid-ossp |
    And the following schemas exist on the hasura database
      | schema      |
      | hdb_catalog |
      | hdb_views   |

  # TODO: we only need a master postgres node, no slave

  Scenario: Any change done on primary database gets reflected on secondary database

    When the api developer creates table 'primary_table' on the primary database
    Then she sees table 'primary_table' in the secondary database

  Scenario: Secondary database is read-only

    When the api developer creates table 'secondary_table' on the secondary database
    Then she gets the error
    """
    cannot execute CREATE TABLE in a read-only transaction
    """
