Feature: The faas engine

  The faas engine allows to bind hasura actions and  
  events to functions.

  Background: Docker node is available

    Given a jelastic environment with an ubuntu-git docker node
    And the faas engine is installed

  Scenario: Log on faas engine

    The log-on credentials are located under  
    `/var/lib/faasd/secrets/`.

    When a user logs on the faas engine
    Then she gets a success response

  Scenario: Deploy new function

    Given a user is logged on the faas engine
    When she deploys the 'hello-python' function to the faas engine
    Then she gets a success response

  Scenario: Call function

    Given the 'hello-python' function has been deployed on the faas engine
    When a user invokes it with payload 'it is me'
    Then she gets http status 200
    And she gets content
      """
      Hello! You said: it is me

      """

  # TODO: test that the login and token-validation functions are READY

  # TODO: test that we get the right Auth API Key + Auth URL out of the functions  