Feature: Fusionauth auth module

  Fusionauth is one of the possible Identity  
  and Authorization Management (IAM) modules.  
  It is used to generate JWTs that are  
  compatible with hasura.

  Background: Jelastic environment ready

    Given a jelastic environment with a database and fusionauth

  Scenario: Fusionauth works without kick-starting

    Without kick-start, the user needs to manually  
    configure fusionauth through its UI.

    When a user installs the fusionauth manifest without kick-starting
    Then fusionauth is up and running

  Scenario: Fusionauth works with kick-starting

    With kick-start, the user can pre-configure  
    fusionauth with a [json file](http://gitlab.hidora.com/softozor/hasura-jps/-/raw/master/features/data/fusionauth/kickstart.json).

    When a user installs the fusionauth manifest with kick-starting
    Then fusionauth is up and running