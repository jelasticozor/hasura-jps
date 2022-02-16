@fixture.default-jelastic-env
@fixture.api-developer
Feature: Hasura environment is well-defined

  As an API developer,  
  I want to base on hasura  
  to build my software.

  The requirements for hasura are documented [here](https://hasura.io/docs/latest/graphql/core/deployment/postgres-requirements.html).

  Scenario: Fusionauth is up

    Then fusionauth is available

  Scenario: The faas engine is up  

    Then the faas engine is available

  Scenario: Hasura is up  

    Then hasura is available

  Scenario: The IAM functions are well-defined

    Then the login function is ready
    And the validate-token function is ready
    And the faas functions find the 'Auth Serverless API Key' in the 'auth-secret'
    And the faas functions find the 'Data Protection Secret Key' in the 'data-protection-secret'

  Scenario: The Jelastic environment is well-defined

    Then there is 1 docker node in the faas node group
    And there are 2 postgres13 nodes in the sqldb node group
    And there is 1 docker node in the cp node group
    And there is 1 nginx-dockerized node in the bl node group

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

  Scenario: Postgres is at least version 10

    Then the postgres version is 13
