# # use up to date driver

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeService(ChromeDriverManager().install()))
import os
import time
import json
import logging

import selenium
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

# from selenium.webdriver.support.wait import WebDriverWait
# def document_initialised(driver):
#     return driver.execute_script("return initialised")

def get_weather_data():
    # CYCLE START
    print("getting weather station data")
    #service = Service(executable_path=os.path.relpath("WebDriver/chromedriver.exe"))
    driver = webdriver.Chrome(executable_path=os.path.relpath("WebDriver/chromedriver.exe"))
    #driver.maximize_window()
    delay = 20 # seconds
    
    try:
        driver.get("https://www.mgm.gov.tr/sondurum/turkiye.aspx")
    except WebDriverException:
        print("get tamamlanmadi")

    try:
        checkpoint1 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[local-name()='svg']//*[local-name()='g']//*[local-name()='path' and contains(@d,'185z')]")))
        print("checkpoint 1")
    except selenium.common.exceptions.TimeoutException:
        print("checkpoint 1 zaman asimi")

    try:
        checkpoint2 = WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element((By.XPATH, "//div[@id='ilAyrintiLabel']/span"), "Ankara"))
        print("checkpoint 2")
    except selenium.common.exceptions.TimeoutException:
        print("checkpoint 2 failed")
    
    
    region = driver.find_element_by_xpath("//*[local-name()='svg']//*[local-name()='g']//*[local-name()='path' and contains(@d,'185z')]")
    print("region ok")
    region.click()
    print("region clicked")

    attemps = 0;
    while attemps < 10:
        try: 
            print(f'{attemps}/10 on click try')
            myCheck = WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element((By.XPATH, "//div[@id='ilAyrintiLabel']/span"), "TEKİRDAĞ"))
            print("data listing ok") 
        except selenium.common.exceptions.TimeoutException:
            print("timeout data listing")
            print(driver.find_element(By.XPATH, ".//td/span[@ng-bind='sndrm.istInfo.istAd']").text)
            attemps += 1
            region.click()

    attemps = 0;
    while attemps < 10:
        print(attemps)
        datarows = driver.find_elements(By.XPATH,"//div[@id='ayrinti']/table/tbody/tr[@class='ng-scope']")
        try:
            checking = True
            for no, row in enumerate(datarows):
                state = row.is_displayed()
                if state == False:
                    print(f' {no:5} element is stale') 
                checking = state and checking
            if not checking:
                print(f' stale element @{no} if found, retrying... ')
                attemps += 1
            else:
                break
        except selenium.common.exceptions.StaleElementReferenceException:
            print(f' stale element @{no} exception found, retrying... ')
            attemps += 1

    results = {}
    resultsState = True

    # result[station]
    for row in datarows:
        #station
        try:
            station = row.find_element(By.XPATH, ".//td/span[@ng-bind='sndrm.istInfo.istAd']").text
            station = "NoInfo" if station=="" else station
        except selenium.common.exceptions.NoSuchElementException:
            station = "NoInfo"
            print("no station")
        except selenium.common.exceptions.StaleElementReferenceException:
            print(" station stale ")
            resultsState = False
            break
        #moment
        try:        
            moment = row.find_element(By.XPATH, ".//td/span[@ng-bind='sndrm.data.veriZamani | meteorDateFormat']").text
            moment = "NoInfo" if moment=="" else moment
        except selenium.common.exceptions.NoSuchElementException:
            moment = "NoInfo"
            print("no moment")
        except selenium.common.exceptions.StaleElementReferenceException:
            print(" moment stale ")
            resultsState = False
            break
        #elevation
        try:
            elevation = row.find_element(By.XPATH, ".//td/span/span[@ng-bind='sndrm.istInfo.yukseklik']").text
            elevation = "NoInfo" if elevation=="" else elevation
        except selenium.common.exceptions.NoSuchElementException:
            elevation = "NoInfo"
            print("no elevation")
        except selenium.common.exceptions.StaleElementReferenceException:
            print(" elevation stale ")
            resultsState = False
            break
        #weather
        try:        
            weather = row.find_element(By.XPATH, ".//td/img[contains(@ng-src, 'hadiseler')]").get_attribute("title")
            weather = "NoInfo" if weather=="" else weather
        except selenium.common.exceptions.NoSuchElementException:
            weather = "NoInfo"
            print("no weather")
        except selenium.common.exceptions.StaleElementReferenceException:
            print(" weather stale ")
            resultsState = False
            break
        #temperature
        try:
            temperature = row.find_element(By.XPATH, ".//td[@ng-bind='sndrm.data.sicaklik | kaliteKontrol | setDecimal:1 | comma']").text
            temperature = "NoInfo" if temperature=="" else temperature
        except selenium.common.exceptions.NoSuchElementException:
            temperature = "NoInfo"
            print("no temperature")
        except selenium.common.exceptions.StaleElementReferenceException:
            print(" temperature stale ")
            resultsState = False
            break
        #rainfall
        try:
            rainfall = row.find_element(By.XPATH, ".//td/span[contains(@ng-bind, 'sndrm.data.yagis00Now')]").text
            rainfall = "NoInfo" if rainfall=="" else rainfall
        except selenium.common.exceptions.NoSuchElementException:
            rainfall = "NoInfo"
            print("no rainfall")
        except selenium.common.exceptions.StaleElementReferenceException:
            print(" rainfall stale ")
            resultsState = False
            break
        #wind
        try:
            wind = row.find_element(By.XPATH, ".//td/span/div/img").get_attribute("style")
            wind = "NoInfo" if wind == "" else wind
        except selenium.common.exceptions.NoSuchElementException:
            wind = "NoInfo"
            print("no wind")
        except selenium.common.exceptions.StaleElementReferenceException:
            print(" wind stale ")
            resultsState = False
            break
        #windspeed
        try:
            windspeed = row.find_element(By.XPATH, ".//td/span[contains(@ng-bind,'sndrm.data.ruzgarHiz')]").text
            windspeed = "NoInfo" if windspeed == "" else windspeed
        except selenium.common.exceptions.NoSuchElementException:
            windspeed = "NoInfo"
            print("no windspeed")
        except selenium.common.exceptions.StaleElementReferenceException:
            print(" windspeed stale ")
            resultsState = False
            break
        #humidty
        try:
            humidity = row.find_element(By.XPATH, ".//td[contains(@ng-bind,'sndrm.data.nem')]").text
            humidity = "NoInfo" if humidity == "" else humidity
        except selenium.common.exceptions.NoSuchElementException:
            humidity = "NoInfo"
            print("no humidity")
        except selenium.common.exceptions.StaleElementReferenceException:
            print(" humidty stale ")
            resultsState = False
            break
        #pressureAct
        try:
            pressureAct = row.find_element(By.XPATH, ".//td[contains(@ng-bind,'sndrm.data.aktuelBasinc')]").text
            pressureAct = "NoInfo" if pressureAct=="" else pressureAct
        except selenium.common.exceptions.NoSuchElementException:
            pressureAct = "NoInfo"
            print("no pressureAct")
        except selenium.common.exceptions.StaleElementReferenceException:
            print(" pressureAct stale ")
            resultsState = False
            break
        #pressureRed
        try:
            pressureRed = row.find_element(By.XPATH, ".//td[contains(@ng-bind,'sndrm.data.denizeIndirgenmisBasinc')]").text
            if pressureRed == "":
                pressureRed = "NoInfo"
        except selenium.common.exceptions.NoSuchElementException:
            pressureRed = "NoInfo"
            print("no pressureRed")
        except selenium.common.exceptions.StaleElementReferenceException:
            print(" pressure stale ")
            resultsState = False
            break

        #print(station, moment, elevation, weather, temperature, rainfall, wind, windspeed, humidity, pressureAct, pressureRed)
        results[station] = {}
        if resultsState:
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
    return resultsState, results
    # CYCLE END

if __name__=='__main__':
    #data = get_weather_data()
    storage = {}

    numberOfGatherings = 144
    waitBetweenTrialsMin = 10 
    for rep in range(numberOfGatherings):
        print(f'GATHERING {rep:5} of {numberOfGatherings:5} started')
        datastate, data = get_weather_data()
        if datastate:
            for i in data:
                if i not in storage:
                    storage[i] = data[i]
                else:
                    theMoment = list(data[i]["measurement"].keys())[0]
                    if theMoment not in storage[i]["measurement"]:
                        storage[i]["measurement"][theMoment] = data[i]["measurement"][theMoment]
            with open("data"+str(rep)+".json", "w") as write_file:
                json.dump(storage, write_file)
        print(f'GATHERING {rep:5} of {numberOfGatherings:5} finished. Success: {datastate}')
        print("uyky")
        time.sleep(waitBetweenTrialsMin*60)
        print("uykk")






