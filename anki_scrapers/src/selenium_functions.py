from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_proxy_list():
  options = webdriver.ChromeOptions()
  options.add_argument("start-maximized")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_experimental_option('useAutomationExtension', False)
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  driver.get("https://sslproxies.org/")
  proxies = [[td.get_attribute('innerHTML') for td in tr.find_elements(By.TAG_NAME, 'td')][:2] for tr in driver.find_element(By.TAG_NAME, 'table').find_elements(By.TAG_NAME, 'tr')][1:]
  driver.quit()
  return [':'.join(proxy) for proxy in proxies]

