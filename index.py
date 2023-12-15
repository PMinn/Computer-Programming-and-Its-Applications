from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import time


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
    with pd.ExcelWriter('肇因.xlsx') as writer:
        for schoolName in data:
            pd.DataFrame(data[schoolName]['肇因']).T.to_excel(writer, schoolName)
    with pd.ExcelWriter('年齡.xlsx') as writer:
        for schoolName in data:
            pd.DataFrame(data[schoolName]['年齡']).T.to_excel(writer, schoolName)
    input("任意輸入下滑...")
    # while True:
    #     temp = height
    #     body.send_keys(Keys.PAGE_DOWN)
    #     time.sleep(0.1)
    #     height = browser.execute_script("return this.scrollY")
    #     print(f"temp:{temp}, height:{height}")
    #     if temp == height:
    #         btnNext = browser.find_elements(
    #             By.CLASS_NAME,
    #             "Buttonstyled__ButtonStyled-sc-5gjk6l-0.jyyvGo.btn.pagination2__next",
    #         )
    #         if len(btnNext) != 0:
    #             btnNext[0].click()
    #         else:
    #             break
    # input("任意輸入結束...")
