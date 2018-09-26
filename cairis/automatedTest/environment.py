from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def before_scenario(context, scenario):
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--window-size=1920x1080")
  browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver")
  context.browser = browser

def after_scenario(context, scenario):
 context.browser.quit()
