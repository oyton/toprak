# # use up to date driver

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeService(ChromeDriverManager().install()))
import os
import time
import json

import selenium
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# def document_initialised(driver):
#     return driver.execute_script("return initialised")

def get_weather_data():
    # CYCLE START

    #service = Service(executable_path=os.path.relpath("WebDriver/chromedriver.exe"))

    driver = webdriver.Chrome(executable_path=os.path.relpath("WebDriver/chromedriver.exe"))
    #driver.maximize_window()
    driver.implicitly_wait(10)


    driver.get("https://www.mgm.gov.tr/sondurum/turkiye.aspx")

    region = driver.find_element_by_xpath("//*[local-name()='svg']//*[local-name()='g']//*[local-name()='path' and contains(@d,'185z')]")
    region.click()
    # WebDriverWait(driver, timeout=10).until(document_initialised)
    attemps = 0;
    while attemps < 10:
        print(attemps)
        datarows = driver.find_elements(By.XPATH,"//div[@id='ayrinti']/table/tbody/tr[@class='ng-scope']")
        try:
            if not datarows[0].is_displayed():
                print("tekrar")
                attemps += 1
            else:
                break
        except selenium.common.exceptions.StaleElementReferenceException:
            print("tekrarr")
            attemps += 1

    results = {}#{"station":{"name":"","elevation":"", "measurement":{"moment":"", "weather":"","temperature":"","rainfall":"", "wind":"", "windspeed":"", "humidty":"", "pressureAct":"", "pressureRed":""}}}

    # result[station]
    for row in datarows:
        try:
            station = row.find_element(By.XPATH, ".//td/span[@ng-bind='sndrm.istInfo.istAd']").text
            station = "NoInfo" if station=="" else station
        except selenium.common.exceptions.NoSuchElementException:
            station = "NoInfo"
            print("no station")
        try:        
            moment = row.find_element(By.XPATH, ".//td/span[@ng-bind='sndrm.data.veriZamani | meteorDateFormat']").text
            moment = "NoInfo" if moment=="" else moment
        except selenium.common.exceptions.NoSuchElementException:
            moment = "NoInfo"
            print("no moment")
        try:
            elevation = row.find_element(By.XPATH, ".//td/span/span[@ng-bind='sndrm.istInfo.yukseklik']").text
            elevation = "NoInfo" if elevation=="" else elevation
        except selenium.common.exceptions.NoSuchElementException:
            elevation = "NoInfo"
            print("no elevation")
        try:        
            weather = row.find_element(By.XPATH, ".//td/img[contains(@ng-src, 'hadiseler')]").get_attribute("title")
            weather = "NoInfo" if weather=="" else weather
        except selenium.common.exceptions.NoSuchElementException:
            weather = "NoInfo"
            print("no weather")
        try:
            temperature = row.find_element(By.XPATH, ".//td[@ng-bind='sndrm.data.sicaklik | kaliteKontrol | setDecimal:1 | comma']").text
            temperature = "NoInfo" if temperature=="" else temperature
        except selenium.common.exceptions.NoSuchElementException:
            temperature = "NoInfo"
            print("no temperature")
        try:
            rainfall = row.find_element(By.XPATH, ".//td/span[contains(@ng-bind, 'sndrm.data.yagis00Now')]").text
            rainfall = "NoInfo" if rainfall=="" else rainfall
        except selenium.common.exceptions.NoSuchElementException:
            rainfall = "NoInfo"
            print("no rainfall")
        try:
            wind = row.find_element(By.XPATH, ".//td/span/div/img").get_attribute("style")
            wind = "NoInfo" if wind == "" else wind
        except selenium.common.exceptions.NoSuchElementException:
            wind = "NoInfo"
            print("no wind")
        try:
            windspeed = row.find_element(By.XPATH, ".//td/span[contains(@ng-bind,'sndrm.data.ruzgarHiz')]").text
            windspeed = "NoInfo" if windspeed == "" else windspeed
        except selenium.common.exceptions.NoSuchElementException:
            windspeed = "NoInfo"
            print("no windspeed")
        try:
            humidity = row.find_element(By.XPATH, ".//td[contains(@ng-bind,'sndrm.data.nem')]").text
            humidity = "NoInfo" if humidity == "" else humidity
        except selenium.common.exceptions.NoSuchElementException:
            humidity = "NoInfo"
            print("no humidity")
        try:
            pressureAct = row.find_element(By.XPATH, ".//td[contains(@ng-bind,'sndrm.data.aktuelBasinc')]").text
            pressureAct = "NoInfo" if pressureAct=="" else pressureAct
        except selenium.common.exceptions.NoSuchElementException:
            pressureAct = "NoInfo"
            print("no pressureAct")
        try:
            pressureRed = row.find_element(By.XPATH, ".//td[contains(@ng-bind,'sndrm.data.denizeIndirgenmisBasinc')]").text
            if pressureRed == "":
                pressureRed = "NoInfo"
        except selenium.common.exceptions.NoSuchElementException:
            pressureRed = "NoInfo"
            print("no pressureRed")

        #print(station, moment, elevation, weather, temperature, rainfall, wind, windspeed, humidity, pressureAct, pressureRed)
        results[station] = {}
        results[station]["elevation"] = elevation
        results[station]["measurement"] = {}
        results[station]["measurement"][moment]={}
        results[station]["measurement"][moment]["weather"] = weather
        results[station]["measurement"][moment]["temperature"] = temperature
        results[station]["measurement"][moment]["rainfall"] = rainfall
        results[station]["measurement"][moment]["wind"] = wind
        results[station]["measurement"][moment]["windspeed"] = windspeed
        results[station]["measurement"][moment]["humidty"] = humidity
        results[station]["measurement"][moment]["pressureAct"] = pressureAct
        results[station]["measurement"][moment]["pressureRed"] = pressureRed

    driver.quit()
    return results
    # CYCLE END

 #data = get_weather_data()
storage = {}

for rep in range(24):
    data = get_weather_data()
    for i in data:
        if i not in storage:
            storage[i] = data[i]
        else:
            theMoment = list(data[i]["measurement"].keys())[0]
            if theMoment not in storage[i]["measurement"]:
                storage[i]["measurement"][theMoment] = data[i]["measurement"][theMoment]
    with open("data"+str(rep)+".json", "w") as write_file:
        json.dump(storage, write_file)
    print("uyky")
    time.sleep(600)
    print("uykk")

#with open("test.html", "w", encoding="utf-8") as f:
#    f.write(page_source)
#f.close()
#tekirdagLink = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[1]/div[2]/div[3]/svg/g/path[86]")
# //*[@id="map"]/div[2]/div[3]/svg/g/path[99]




