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

from behave import *
from GenericSteps import *

__author__ = 'Nathan Jenkins'


@given('I have navigated to the CAIRIS web application')
def step_impl(context):
  NavigateToApp(context)

@when('I supply valid credentials')
def step_impl(context):
  EnterValidCredentials(context)

@then('I am granted access to the application')
def step_impl(context):
  LoggedIn(context)

@when('I supply {username} and {password}')
def step_impl(context, username, password):
  EnterCredentials(context, username, password)
  ClickButtonWithId(context, 'submit')

@then('I am refused access to the application')
def step_impl(context):
  assert OnLandingPage(context) is True

@given('I have successfully authenticated with CAIRIS')
def step_impl(context):
  NavigateToApp(context)
  EnterValidCredentials(context)
  LoggedIn(context)

@when('I click logout')
def step_impl(context):
  logout = context.browser.find_element_by_id('logoutClick')
  logout.click()

@then('I am returned to the landing page')
def step_impl(context):
  assert OnLandingPage(context) is True

def LoggedIn(context):
  WaitForSpinningWheelOfDoom(context)
  ClickButtonWithId(context, 'homeClick')

def OnLandingPage(context):
  WaitForVisibleById(context, 'email')
  WaitForVisibleById(context, 'password')
  return True 
