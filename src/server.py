# coding=utf-8
from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import export
from chart import barPlot
import dataFormatter
from scraper import run


app = Flask(__name__, static_url_path="/static")
port = 8088
CORS(app)


@app.route("/api/analysis", methods=["POST"])
def analysis():
    selectedSchool = request.json
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
    barPlot('./static/count.jpg', barData, labels, figsize=(int(len(labels)*len(barData)), 5), total_width=.8, single_width=.9)
    causeData, labels = dataFormatter.toCauseData(data)
    barPlot('./static/cause.jpg',causeData, labels, figsize=(int(len(labels)*len(causeData)), 5), total_width=.8, single_width=.9)
    ageData, labels = dataFormatter.toAgeData(data)
    barPlot('./static/age.jpg', ageData, labels, figsize=(int(len(labels)*len(ageData)), 5), total_width=.8, single_width=.9)
    
    return jsonify(data)


if __name__ == "__main__":
    app.run(port=port, debug=True)
