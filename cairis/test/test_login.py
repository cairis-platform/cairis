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

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

__author__ = 'Huynh Le, Shamal Faily'

class LoginTest(unittest.TestCase):

  def setUp(self):
    pass

  def test_login(self):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/tmp/chromedriver")

    driver.get("https://demo.cairis.org")

    driver.find_element_by_id('email').send_keys('test')
    driver.find_element_by_id('password').send_keys('test')
    driver.find_element_by_id('password').send_keys(Keys.RETURN)

    aboutElem = driver.find_element_by_id('aboutClick')
    self.assertIsInstance(aboutElem,webdriver.remote.webelement.WebElement)
    driver.find_element_by_id('logoutClick').click()

    driver.find_element_by_id('email').send_keys('test')
    driver.find_element_by_id('password').send_keys('wrongpassword')
    driver.find_element_by_id('password').send_keys(Keys.RETURN)
    
    with self.assertRaises(NoSuchElementException):
      driver.find_element_by_id('aboutClick')
    
  def tearDown(self):
    pass

if __name__ == '__main__':
    unittest.main()

