#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import *
from subscript import book1, book2


username = input('username:')
password = getpass.getpass()


def login_unipus(d):
    d.implicitly_wait(2)
    d.get('http://10.81.0.88/index.php')
    try:
        d.find_element_by_id('username').send_keys(username)
        d.find_element_by_id('password').send_keys(password)
        sleep(0.2)
        d.find_element_by_xpath('//*[@id="layui-layer1"]/span/a').click()
        d.find_element_by_xpath('//*[@id="LoginForm"]/table/tbody/\
                tr[3]/td[2]/input').click()
    except NoSuchElementException:
        pass
    d.implicitly_wait(3)


def for_unipus(d):
    login_unipus(d)
    book1.run(d)
    login_unipus(d)
    book2.run(d)


if __name__ == '__main__':
    d = webdriver.Chrome()
    d.implicitly_wait(2)
    for_unipus(d)
    d.close()


