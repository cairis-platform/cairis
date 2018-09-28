#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#
#  Author: Nathan Jenkins

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
