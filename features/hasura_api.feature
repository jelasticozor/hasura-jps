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
  Scenario: Hasura is up and running

    When the user applies the database migrations of the 'todo_project'
    Then she gets success

  @wip  
  Scenario: Hasura is again available after container restart

    Given the cp containers have been restarted
    When the user assesses hasura's liveness
    Then she gets 'OK'

  @wip  
  Scenario: The hasura API is working

    #  hasura migrate apply --database-name default --admin-secret cYcnIpUJhdsdRskAFgp6 --endpoint http://node94933-jelasticozor.hidora.com:11106 --project todo_project
    #  hasura metadata apply --admin-secret cYcnIpUJhdsdRskAFgp6 --endpoint http://node94933-jelasticozor.hidora.com:11106 --project todo_project

    Given the user has applied the database migrations of the 'todo_project'
    And its database metadata
    And she has added the following todo:
      | title       | make hasura work                              |
      | description | we need a jelastic manifest to install hasura |
    # TODO: rather show and run the corresponding graphql query here
    When she retrieves the todo entitled 'make hasura work'
    Then she gets the description
    """
    we need a jelastic manifest to install hasura
    """

  #  TODO: test eventing (call api endpoint which triggers an event which sets a value in the db; assert that the value has been set)

  # TODO: try to log on as a user with some permissions and generate a jwt
