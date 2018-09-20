import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class LoginGUITest(unittest.TestCase):

  def setUp(self):
    pass

  def testLoginGUI(self):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver")

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

