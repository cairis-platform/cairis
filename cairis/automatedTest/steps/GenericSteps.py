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

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException

__author__ = 'Nathan Jenkins'

validUsername = 'test'
validPassword = 'test'

def NavigateToApp(context):
  context.browser.get("https://demo.cairis.org")

def EnterValidCredentials(context):
  EnterCredentials(context, validUsername, validPassword)
  ClickButtonWithId(context, 'submit')

def EnterCredentials(context, username, password):
  usernameEl = FindElementById(context, 'email')
  passwordEl = FindElementById(context, 'password')
  
  EnterText(usernameEl, username)
  EnterText(passwordEl, password)

def ClickButtonWithId(context, id):
  button = FindElementById(context, id)
  button.click()

def FindElementById(context, id):
  return context.browser.find_element_by_id(id)

def EnterText(element, text):
  element.send_keys(text)

def ElementWithIdInvisible(context, id):
  elelement = FindElementById(context, id);
  assert element.is_displayed is False

def WaitForSpinningWheelOfDoom(context):
  spinningWheelOfDoom = 'displayWrapper'
  WaitForInvisibleByClass(context, 'divLoading')

def WaitForVisibleByClass(context, className):
  return WaitForVisibleStateByClass(context, className, True)

def WaitForInvisibleByClass(context, className):
  return WaitForVisibleStateByClass(context, className, False)

def WaitForVisibleStateByClass(context, className, displayState):
  if(displayState == True):
    element = WebDriverWait(context.browser, 30, 0.5, (ElementNotVisibleException)).until(lambda x: x.find_element_by_class_name(className).is_displayed())
  else:
    element = WebDriverWait(context.browser, 30, 0.5, (ElementNotVisibleException)).until_not(lambda x: x.find_element_by_class_name(className).is_displayed())
  return element

def WaitForVisibleById(context, id):
  return WaitForVisibleStateById(context, id, True)

def WaitForInvisibleById(context, id):
  return WaitForVisibleStateById(context, id, False)

def WaitForVisibleStateById(context, id, displayState):
  if(displayState == True):
    element = WebDriverWait(context.browser, 30, 0.5, (ElementNotVisibleException)).until(lambda x: x.find_element_by_id(id).is_displayed())
  else:
    element = WebDriverWait(context.browser, 30, 0.5, (ElementNotVisibleException)).until_not(lambda x: x.find_element_by_id(id).is_displayed())
  return element
