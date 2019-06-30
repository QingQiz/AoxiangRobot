#!/usr/bin/env python3

import json
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import *
from functions import getUserName_Password

userName, password = getUserName_Password.get(is_input=False)

option = webdriver.ChromeOptions()
# option.add_argument('headless')
d = webdriver.Chrome(options=option)
d.get('http://us.nwpu.edu.cn/eams/login.action')

while True:
    try:
        d.find_element_by_id('username').send_keys(userName)
        d.find_element_by_id('password').send_keys(password)
        d.find_element_by_id('local_zh').click()
        d.find_element_by_class_name('submit_button').click()
        break
    except NoSuchElementException:
        sleep(1)

d.delete_cookie('semester.id')
d.add_cookie({'name': 'semester.id', 'value': '19', 'path': '/eams/'})
d.get('http://us.nwpu.edu.cn/eams/')
sleep(1)

res = []
dic = {
    "星期一": "1",
    "星期二": "2",
    "星期三": "3",
    "星期四": "4",
    "星期五": "5",
    "星期六": "6",
    "星期日": "7",
}
while True:
    try:
        xpath = '/html/body/div[2]/div[3]/div[3]/div[1]/table/tbody/tr/td/div/div/table/tbody'
        table = d.find_element_by_xpath(xpath)
        trs = len(d.find_elements_by_xpath(xpath + '/tr[*]'))
        #       课程名称 安排 起止周 教师
        infoIndex = [4,   8,    9,    5]

        for i in range(trs):
            data = lambda y: \
                    d.find_element_by_xpath(xpath + '/tr[{}]/td[{}]'.format(i + 1, infoIndex[y])).text

            if data(3) == '在线开放课程':
                continue
            for c in data(1).split('\n'):
                name = data(0)
                week = data(2).split('-')
                infoList = c.split(' ')
                time = infoList[2].split('-')

                res.append({
                    "name": name,
                    "week": {
                        "start": week[0],
                        "end": week[1]
                    },
                    "day": dic[infoList[1]],
                    "time": {
                        "start": time[0],
                        "end": time[1],
                    },
                    "room": infoList[-1]
                })

        print(res)
        with open('settings/classInfo.json', 'w') as f:
            json.dump(res, f, indent=4, ensure_ascii=False)

        break
    except NoSuchElementException:
        sleep(1)

d.close()
