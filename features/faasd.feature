Feature: Install faas engine

  The faas engine will allow to bind hasura actions and
  events to functions.

  Background: VPS node is available

    Given a jelastic environment with a node of type 'ubuntu-vps' is available

  Scenario: The faas engine installs successfully

    When the faas engine gets installed on the node of type 'ubuntu-vps'
    Then the installation is successful

  Scenario: Log on

    Given the faas engine is installed on the node of type 'ubuntu-vps'
    When a user logs on the faas engine
    Then she gets a success response

# TODO: in the main manifest we need to test that the faasd comes in a node with nodetype == ubuntu-vps and nodegroup == vps