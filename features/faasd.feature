Feature: Install faas engine

  The faas engine will allow to bind hasura actions and
  events to functions.

  Background: Docker node is available

    Given a jelastic environment with a docker node is available in group 'faas' with image 'softozor/ubuntu-git:latest'
    And the faas engine is installed

  Scenario: Log on

    When a user logs on the faas engine
    Then she gets a success response

  Scenario: Deploy new function

    When a user deploys the 'hello-python' function to the faas engine
    Then she gets a success response

  Scenario: Call function

    Given the 'hello-python' function has been deployed on the faas engine
    When a user invokes it with payload 'it is me'
    Then she gets http status 200
    And she gets content
      """
      Hello! You said: it is me
      """