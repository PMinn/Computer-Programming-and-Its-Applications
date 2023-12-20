# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import export
import dataFormatter
from chart import barPlot
from scraper import run


if __name__ == "__main__":
    # 爬取資料
    selectedSchool = [{"city":{"text":"臺中市","value":"15"},"school":{"text":"逢甲大學","value":"21168:POINT (13430574.1967 2775198.2921000011)"}},{"city":{"text":"臺中市","value":"15"},"school":{"text":"東海大學","value":"21169:POINT (13425014.6006 2775277.2644000016)"}},{"city":{"text":"臺中市","value":"15"},"school":{"text":"僑光科技大學","value":"21164:POINT (13429953.322299998 2776456.0414000005)"}}]
    for i in range(len(selectedSchool)):
        selectedSchool[i]['label'] = selectedSchool[i]['school']['text'] + '(' + selectedSchool[i]['city']['text'] + ')'
    browser = webdriver.Chrome(service=Service("../chromedriver/chromedriver.exe"))
    browser.get("https://roadsafety.tw/SchoolHotSpots")
    browser.execute_script("setInterval(() => [...document.querySelectorAll('.modal.show .close')].forEach(e => e.click()), 300)")
    data = run(browser, selectedSchool)

    # 儲存成Excel
    export.toExcel(data, '肇因')
    export.toExcel(data, '年齡')

    # 繪製圖表
    barData, labels = dataFormatter.toCountTotal(data, ['死亡', '受傷'])
    barPlot('count.jpg', barData, labels, figsize=(int(len(labels)*len(barData)), 5), total_width=.8, single_width=.9)
    
    causeData, labels = dataFormatter.toCauseData(data)
    barPlot('cause.jpg',causeData, labels, figsize=(int(len(labels)*len(causeData)), 5), total_width=.8, single_width=.9)

    ageData, labels = dataFormatter.toAgeData(data)
    barPlot('age.jpg', ageData, labels, figsize=(int(len(labels)*len(ageData)), 5), total_width=.8, single_width=.9)