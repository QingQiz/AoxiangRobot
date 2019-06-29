#!/usr/bin/env python3

from time import sleep
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.select import Select
from functions import getUserName_Password

userName, password = getUserName_Password.get(default=True)

chromeOption = webdriver.ChromeOptions()
# chromeOption.add_argument('headless')
d = webdriver.Chrome(options=chromeOption)
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
"""
while True:
    try:
        week = d.find_element_by_xpath('//*[@id="Nav_bar"]/div[3]/div').text.split('。')
        today = week[1].strip('\n').split('/')[1].split(',')[0]
        week = week[2].strip('\n').split(' ')[2][1:]
        week = week[0:2] if ('0' <= week[1] <= '9') else week[0:1]
        print(today, week)

        today = "星期三"
        week = "1"
        week_sel = d.find_element_by_xpath('//*[@id="startWeek"]')
        Select(week_sel).select_by_value(week)
        break
    except NoSuchElementException:
        sleep(1)
"""
d.delete_cookie('semester.id')
d.add_cookie({'name': 'semester.id', 'value': '19', 'path': '/eams/'})
d.get('http://us.nwpu.edu.cn/eams/')

res = 'className\tstartWeek\tendWeek\tweekday\tclassEND\tclassSTART\tclassroom\tinterval\n'
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
        #print(d.get_cookies())
        xpath = '/html/body/div[2]/div[3]/div[3]/div[1]/table/tbody/tr/td/div/div/table/tbody'
        table = d.find_element_by_xpath(xpath)
        l = len(d.find_elements_by_xpath(xpath + '/tr[*]'))
        #       课程名称 安排 起止周 教师
        infoIndex = [4,   8,    9,    5]

        for i in range(l):
            data = lambda y: \
                    d.find_element_by_xpath(xpath + '/tr[{}]/td[{}]'.format(i + 1, infoIndex[y])).text

            if data(3) == '在线开放课程':
                continue
            for c in data(1).split('\n'):
                name = data(0)
                res += name + '\t'

                week = data(2).split('-')
                res += week[0] + '\t' + week[1] + '\t'

                infoList = c.split(' ')
                res += dic[infoList[1]] + '\t'
                time = infoList[2].split('-')
                res += time[1] + '\t' + time[0] + '\t'
                res += infoList[-1] + '\t1\n'

        print(res)
        with open('res.tab', 'w') as f:
            f.write(res)

        break
    except NoSuchElementException:
        sleep(1)

d.close()
