# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json


def getTableData(tableID, browser):
    table = browser.find_element(By.ID, tableID)
    data = {}
    keys = [td.get_attribute("innerText") for td in table.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")]
    keys.pop(0)
    for tr in table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr"):
        th = tr.find_element(By.TAG_NAME, "th")
        tds = tr.find_elements(By.TAG_NAME, "td")
        data[th.get_attribute("innerText")] = {}
        for i in range(len(keys)):
            data[th.get_attribute("innerText")][keys[i]] = tds[i].get_attribute("innerText")
    return data


def getUniversityList():
    # 爬取資料
    url = "https://roadsafety.tw/SchoolHotSpots"
    browser = webdriver.Chrome(service=Service("../chromedriver/chromedriver.exe"))
    browser.get(url)
    browser.execute_script("setInterval(() => [...document.querySelectorAll('.modal.show .close')].forEach(e => e.click()), 300)")
    Select(browser.find_element(By.ID, "ddlSchoolType")).select_by_value("10708") # 選擇大專院校
    citySelectElement = browser.find_element(By.ID, "ddlCity")
    citySelect = Select(citySelectElement)
    cityOptionElements = citySelectElement.find_elements(By.TAG_NAME, "option")
    schoolSelectElement = browser.find_element(By.ID, "ddlSchool")
    universityList = []
    for cityOptionElement in cityOptionElements:
        cityValue = cityOptionElement.get_attribute('value')
        cityText = cityOptionElement.get_attribute('innerText')
        citySelect.select_by_value(cityValue)
        time.sleep(0.1)
        for schoolOptionElement in schoolSelectElement.find_elements(By.TAG_NAME, "option"):
            schoolValue = schoolOptionElement.get_attribute('value')
            if len(schoolValue) > 0:
                universityList.append({'school':{'text':schoolOptionElement.get_attribute('innerText'), 'value': schoolValue}, 'city':{'value':cityValue, 'text':cityText}})
    with open('./static/universityList.json', 'w', encoding='utf-8') as file:
        json.dump(universityList, file, ensure_ascii=False)

if __name__ == "__main__":
    main()