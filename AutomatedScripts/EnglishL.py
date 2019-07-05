#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
from selenium import webdriver
from selenium.common.exceptions import *
from subscript import book1, book2


# username = input('username:')
# password = getpass.getpass()
username = '2017302344'
password = '04045912'


def login(d):
    d.implicitly_wait(2)
    d.get('http://10.81.0.88/index.php')
    try:
        d.find_element_by_id('username').send_keys(username)
        d.find_element_by_id('password').send_keys(password)
        d.find_element_by_xpath('//*[@id="LoginForm"]/table/tbody/\
                tr[3]/td[2]/input').click()
    except NoSuchElementException:
        pass
    d.implicitly_wait(3)


if __name__ == '__main__':
    d = webdriver.Chrome()
    d.implicitly_wait(2)

    login(d)
    #book1.run(d)
    # login(d)
    book2.run(d)
    d.close()

