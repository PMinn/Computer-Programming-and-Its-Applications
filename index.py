#coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time


def barPlot(data, tick, colors=None, total_width=0.8, single_width=1):
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    n_bars = len(data)
    bar_width = total_width / n_bars
    bars = []
    for i, (name, values) in enumerate(data.items()):
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
        bar = plt.bar(np.arange(len(values)) + x_offset, values, width=bar_width * single_width, tick_label=tick, label=name, color=colors[i % len(colors)])
        bars.append(bar)
    for bar in bars:
        plt.bar_label(bar, fmt='%.0f', label_type='edge')
    plt.legend(loc='best')


def drawBarChart(data, column):
    label = [schoolName for schoolName in data]
    barData = {}
    for i in range(len(column)):
        attribute = column[i]
        barData[attribute] = [sum([int(data[schoolName]['肇因'][index][attribute]) for index in data[schoolName]['肇因']]) for schoolName in data]
    barPlot(barData, label, total_width=.8, single_width=.9)
    plt.show()


def dataToCauseData(data):
    sumCause = {}
    for schoolName in data:
        for index in data[schoolName]['肇因']:
            if data[schoolName]['肇因'][index]['肇事原因'] not in sumCause:
                sumCause[data[schoolName]['肇因'][index]['肇事原因']] = int(data[schoolName]['肇因'][index]['件數'])
            else:
                sumCause[data[schoolName]['肇因'][index]['肇事原因']] += int(data[schoolName]['肇因'][index]['件數'])
    topFiveCause = sorted(sumCause.items(), key=lambda x: x[1], reverse=True)[:5]
    labels = [cause[0] for cause in topFiveCause]
    causeData = {}
    for schoolName in data:
        causeData[schoolName] = []
        for cause in topFiveCause:
            indexes = [index for index in data[schoolName]['肇因'] if data[schoolName]['肇因'][index]['肇事原因']==cause[0]]
            if len(indexes) == 0:
                causeData[schoolName].append(0)
            else:
                causeData[schoolName].append(int(data[schoolName]['肇因'][indexes[0]]['件數']))
    return causeData, labels


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


if __name__ == "__main__":
    url = "https://roadsafety.tw/SchoolHotSpots"
    browser = webdriver.Chrome(service=Service("chromedriver.exe"))
    browser.get(url)
    data = {'東海大學':{}, '逢甲大學':{}, '僑光科技大學':{}}
    browser.execute_script("setInterval(() => [...document.querySelectorAll('.modal.show .close')].forEach(e => e.click()), 300)")
    body = browser.find_element(By.TAG_NAME, "body")
    Select(browser.find_element(By.ID, "ddlSchoolType")).select_by_value("10708") # 選擇大專院校
    Select(browser.find_element(By.ID, "ddlCity")).select_by_value("15") # 選擇台中市
    for schoolName in data:
        Select(browser.find_element(By.ID, "ddlSchool")).select_by_visible_text(schoolName) # 選擇學校
        browser.find_element(By.ID, "bSearch").click()
        data[schoolName]['肇因'] = getTableData("tbCause", browser)
        data[schoolName]['年齡'] = getTableData("tbAges", browser)

    # 儲存成Excel
    with pd.ExcelWriter('肇因.xlsx') as writer:
        for schoolName in data:
            pd.DataFrame(data[schoolName]['肇因']).T.to_excel(writer, schoolName)
    with pd.ExcelWriter('年齡.xlsx') as writer:
        for schoolName in data:
            pd.DataFrame(data[schoolName]['年齡']).T.to_excel(writer, schoolName)

    causeData, labels = dataToCauseData(data)
    barPlot(causeData, labels)
    plt.show()

    # print(data)
    drawBarChart(data, ['死亡', '受傷'])