#!/usr/bin/env python3

"""
自动评教
"""
import sys
import getpass
from selenium import webdriver
from selenium.common.exceptions import *
from time import sleep

userName = '2017302344'
password = open('.password').read().strip('\n')

if len(sys.argv) == 2:
    if sys.argv[1] == '-i':
        userName = input("UserName:________\b\b\b\b\b\b\b\b")
        password = getpass.getpass('Password:')

d = webdriver.Chrome()
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

d.get('http://us.nwpu.edu.cn/eams/home!childmenus.action?menu.id=165')

while True:
    try:
        d.find_element_by_xpath('//*[@href="/eams/evaluateStd.action"]').click()
        break
    except NoSuchElementException:
        sleep(1)

while True:
    try:
        found = d.find_elements_by_xpath('//*[@id="evaluateForm"]/table/tbody/tr[*]/td[6]/a')
        if len(found) == 0:
            continue
        for i in range(len(found)):
            d.find_element_by_xpath('//*[@id="evaluateForm"]/table/tbody/tr[{}]/td[6]/a'.format(str(i + 1))).click()
            while True:
                radios = d.find_elements_by_xpath('//*[@id="evaluateTB"]/tr[*]/td[3]')
                if len(radios) == 0:
                    continue
                for j in radios:
                    j.find_elements_by_xpath('input')[0].click()
                    sleep(0.1)
                break
            d.find_element_by_id('btnSave').click()
            d.switch_to.alert.accept()
            sleep(1)
        break
    except NoSuchElementException:
        sleep(1)

d.close()
