# # use up to date driver

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeService(ChromeDriverManager().install()))
import os

from selenium.webdriver.chrome.service import Service
from selenium import webdriver

service = Service(executable_path=os.path.relpath("WebDriver/chromedriver.exe"))
driver = webdriver.Chrome(executable_path=os.path.relpath("WebDriver/chromedriver.exe"))

driver.get("https://www.selenium.dev/selenium/web/web-form.html")
