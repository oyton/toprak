# # use up to date driver

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeService(ChromeDriverManager().install()))
import os

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC4



service = Service(executable_path=os.path.relpath("WebDriver/chromedriver.exe"))
driver = webdriver.Chrome(executable_path=os.path.relpath("WebDriver/chromedriver.exe"))
driver.maximize_window()
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)
driver.get("https://www.mgm.gov.tr/sondurum/turkiye.aspx")
#region = WebDriverWait(driver,10).until(EC4.element_to_be_clickable((By.XPATH, "//*[@id='map']/div[2]/div[3]/svg/g/path[99]")))
#region = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[1]/div[2]/div[3]/svg/g/path[86]")
#region = driver.find_element(By.XPATH, "*[@id='map']/div[2]/div[3]/svg/g/path[99]")
driver.implicitly_wait(10)
#region.click()
#driver.implicitly_wait(10)
#page_source = driver.page_source
region = driver.find_element(By.XPATH, "//*[local-name()='svg']//*[local-name()='g']//*[local-name()='path' and @d='M239 187L238 184L240 180L238 177L230 177L230 174L226 171L227 161L224 158L225 156L229 157L234 154L237 149L237 141L239 139L252 141L256 146L262 147L265 138L270 134L287 127L291 129L290 130L293 133L293 138L287 143L284 155L286 158L283 163L278 163L274 160L262 163L260 170L254 175L253 178L245 184L240 185z']")
region.click()


#with open("test.html", "w", encoding="utf-8") as f:
#    f.write(page_source)
#f.close()
#tekirdagLink = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[1]/div[2]/div[3]/svg/g/path[86]")
# //*[@id="map"]/div[2]/div[3]/svg/g/path[99]




