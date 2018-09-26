Feature: Login and Logout
  In order to secure CAIRIS
  As a Product Owner
  I want the application to be secured with a user name and password

  Scenario: Successful Login
    Given I have navigated to the CAIRIS web application
    When I supply valid credentials
    Then I am granted access to the application

  Scenario Outline: Unsuccessful Login
    Given I have navigated to the CAIRIS web application
    When I supply <username> and <password>
    Then I am refused access to the application

  Examples: 
    | username  | password  |  
    | test      | incorrect |  
    | incorrect | test      |  
    | incorrect | incorrect |  

  Scenario: Logout
    Given I have successfully authenticated with CAIRIS
    When I click logout
    Then I am returned to the landing page 