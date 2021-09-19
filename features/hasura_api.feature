# TODO: install the main manifest before the whole feature
Feature: Hasura API

  As a user,
  I want to use the hasura API,
  in order to build my system.

  Background: The main manifest is installed

    Given the user has installed the main manifest

  Scenario: The faas engine is well-defined

    Then there is 1 docker node in the faas node group

  Scenario: The database is deployed in a master-slave architecture

    Then there are 2 postgres13 nodes in the sqldb node group  

  Scenario: The api is deployed in the cp node group

    Then there is 1 docker node in the cp node group

  Scenario: A load balancer is served in front of the compute node

    Then there is 1 nginx-dockerized node in the bl node group

  # TODO: check that the nginx has ssl installed

  @current
  Scenario: Hasura accepts database migrations

    When the user applies the database migrations of the 'todo_project'
    Then she gets success

  Scenario: The hasura API is functional

    Given the user has applied the database migrations of the 'todo_project'
    And its database metadata
    And she adds a todo through the following graphql mutation
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
      }
    }
    """
    Then she gets the description
    """
    we need a jelastic manifest to install hasura
    """

  #  TODO: test eventing (call api endpoint which triggers an event which sets a value in the db; assert that the value has been set)

  # TODO: try to log on as a user with some permissions and generate a jwt
