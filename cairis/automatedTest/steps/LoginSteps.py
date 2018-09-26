from behave import *
from GenericSteps import *

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
