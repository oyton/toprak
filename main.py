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
#driver.maximize_window()
driver.implicitly_wait(10)

# CYCLE START
driver.get("https://www.mgm.gov.tr/sondurum/turkiye.aspx")

driver.implicitly_wait(10)

region = driver.find_element_by_xpath("//*[local-name()='svg']//*[local-name()='g']//*[local-name()='path' and contains(@d,'185z')]")
region.click()

driver.implicitly_wait(10)

datarows = driver.find_elements_by_xpath("//div[@id='ayrinti']/table/tbody/tr[@class='ng-scope']")

for row in datarows:
    station = row.find_elements_by_xpath("//td/span[@ng-bind='sndrm.istInfo.istAd']").text
    height = row.find_elements_by_xpath("//td/span[@ng-bind='sndrm.istInfo.yukseklik']").text


#with open("test.html", "w", encoding="utf-8") as f:
#    f.write(page_source)
#f.close()
#tekirdagLink = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[1]/div[2]/div[3]/svg/g/path[86]")
# //*[@id="map"]/div[2]/div[3]/svg/g/path[99]




