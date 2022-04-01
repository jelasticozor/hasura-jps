@production
@fixture.jelastic-env
@fixture.api-developer
Feature: Production Hasura environment

  As an API developer,  
  I want a hasura environment optimized for production,  
  so that I can expose my software to my customers in the best way.

  The requirements for hasura are documented [here](https://hasura.io/docs/latest/graphql/core/deployment/postgres-requirements.html).
  The recommended hasura setup for production is documented [here](https://hasura.io/docs/latest/graphql/core/deployment/production-checklist.html).

  # TODO: improve this setup

  Scenario: The Jelastic environment is well-defined

    Then the iam engine is up
    And the faas engine is up
    And hasura is up
    And the database has postgres version 13

  Scenario: The IAM functions are well-defined

    Then the sign-in function is ready
    And the validate-token function is ready
    And the faas functions find the 'Auth Serverless API Key' in the 'auth-secret'
    And the faas functions find the 'Data Protection Secret Key' in the 'data-protection-secret'

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

  Scenario: Any change done on primary database gets reflected on secondary database

    When the api developer creates table 'primary_table' on the primary database
    Then she sees table 'primary_table' in the secondary database

  Scenario: Secondary database is read-only

    When the api developer creates table 'secondary_table' on the secondary database
    Then she gets the error
    """
    cannot execute CREATE TABLE in a read-only transaction
    """
