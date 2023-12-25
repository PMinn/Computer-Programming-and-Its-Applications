# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import export
import dataFormatter
from chart import barPlot


def getTableData(className, browser):
    browser.find_element(By.ID, f"tab{className}").click()
    table = browser.find_element(By.ID, f"tb{className}")
    data = {}
    keys = [td.get_attribute("innerText") for td in table.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")]
    keys.pop(0)
    trs = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    for i in range(len(trs)):
        th = trs[i].find_element(By.TAG_NAME, "th")
        tds = trs[i].find_elements(By.TAG_NAME, "td")
        data[str(i + 1)] = {}
        for j in range(len(keys)):
            data[str(i + 1)][keys[j]] = tds[j].get_attribute("innerText")
    return data


def run(browser, selectedSchool):
    Select(browser.find_element(By.ID, "ddlSchoolType")).select_by_value("10708") # 選擇大專院校
    data = {}
    for school in selectedSchool:
        data[school['label']] = {}
        Select(browser.find_element(By.ID, "ddlCity")).select_by_value(school['city']['value']) # 選擇縣市
        time.sleep(0.5)
        Select(browser.find_element(By.ID, "ddlSchool")).select_by_value(school['school']['value']) # 選擇學校
        browser.find_element(By.ID, "bSearch").click()
        time.sleep(0.5)
        data[school['label']]['肇因'] = getTableData("Cause", browser)
        data[school['label']]['年齡'] = getTableData("Ages", browser)
    return data


if __name__ == "__main__":
    selectedSchool = [{"city":{"text":"臺北市","value":"13"},"school":{"text":"東吳大學城中校區","value":"21091:POINT (13526392.792000003 2880452.5984000005)"}},{"city":{"text":"臺北市","value":"13"},"school":{"text":"法務部司法官學院","value":"21090:POINT (13530508.0238 2878189.7652000003)"}}]
    for i in range(len(selectedSchool)):
        selectedSchool[i]['label'] = selectedSchool[i]['school']['text'] + '(' + selectedSchool[i]['city']['text'] + ')'
    browser = webdriver.Chrome(service=Service("../chromedriver/chromedriver.exe"))
    browser.get("https://roadsafety.tw/SchoolHotSpots")
    browser.execute_script("setInterval(() => {[...document.querySelectorAll('.modal.show .close')].forEach(e => e.click());document.querySelector('#Result .card-body').scrollTop+=50;}, 300)")
    data = run(browser, selectedSchool)

    # 儲存成Excel
    export.toExcel(data, './static', '肇因')
    export.toExcel(data, './static', '年齡')

    # 繪製圖表
    barData, labels = dataFormatter.toCountTotal(data, ['死亡', '受傷'])
    barPlot('./static/count.jpg', barData, labels, figsize=(len(labels)*max(len(barData), 3), 5), total_width=.8, single_width=.9)
    
    causeData, labels = dataFormatter.toCauseData(data)
    barPlot('./static/cause.jpg',causeData, labels, figsize=(max(len(labels), 3)*len(causeData), 5), total_width=.8, single_width=.9)

    ageData, labels = dataFormatter.toAgeData(data)
    barPlot('./static/age.jpg', ageData, labels, figsize=(len(labels)*max(len(ageData), 3), 5), total_width=.8, single_width=.9)