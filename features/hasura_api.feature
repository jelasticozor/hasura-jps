Feature: Hasura API

  As a manifest user,  
  I want to base on hasura  
  to build my software.

  The requirements for hasura are documented [here](https://hasura.io/docs/latest/graphql/core/deployment/postgres-requirements.html).

  Background: The main manifest is installed

    Given the user has installed the main manifest

  Scenario: The Jelastic environment is well-defined

    Then there is 1 docker node in the faas node group
    And there are 2 postgres13 nodes in the sqldb node group  
    And there is 1 docker node in the cp node group
    And there is 1 nginx-dockerized node in the bl node group

  # TODO: check that the nginx has ssl installed

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

  Scenario: Hasura accepts database migrations

    This is one way to check that hasura is up and running.

    When the user applies the database migrations of the 'todo_project'
    Then she gets success

  Scenario: The hasura API is functional

    After successful installation, hasura makes a graphql API  
    available. Here we install a simple todo project and try to  
    query a todo after its successful insertion into the database.

    Given the user has applied the database migrations of the 'todo_project'
    And its database metadata
    And she has added a todo through the following graphql mutation
    """
    mutation {
      insert_todos_one(object: {
        title: "make hasura work"
        description: "we need a jelastic manifest to install hasura"
      }) {
        id
      }
    }
    """
    When she retrieves the new todo with the following query
    """
    query GetTodo ($id: uuid!) {
      todos_by_pk (id: $id) {
        description
        state
      }
    }
    """
    Then she gets the description
    """
    we need a jelastic manifest to install hasura
    """
    And state 'NEW'

  Scenario: The faas engine integrates with hasura API

    The faas engine makes serverless functions available for  
    binding with hasura actions or events. Here we call our  
    test `do` mutation which calls the `hasura-action` function  
    on the faas engine through the mechanism of hasura actions.  
    The `hasura-action` function changes a todo's state to  
    `DOING`.

    Given the 'hasura-action' function has been deployed on the faas engine
    And the user has applied the database migrations of the 'todo_project'
    And its database metadata
    And she has added a todo through the following graphql mutation
    """
    mutation {
      insert_todos_one(object: {
        title: "make hasura work"
        description: "we need a jelastic manifest to install hasura"
      }) {
        id
      }
    }
    """
    And the user has started the todo with the hasura action
    """
    mutation Do ($id: uuid!) {
      do(id: $id) {
        state
      }
    }
    """
    When she retrieves the new todo with the following query
    """
    query GetTodo ($id: uuid!) {
      todos_by_pk (id: $id) {
        state
      }
    }
    """
    Then she gets state 'DOING'

  # TODO: try to log on as a user with some permissions and call a mutation requiring that permission (e.g. delete todo)
  # --> should work

  # TODO: try to call the mutation requiring permission without permission