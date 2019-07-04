#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import re
from selenium import webdriver
from selenium.common.exceptions import *
from time import sleep


# username = input('username:')
# password = getpass.getpass()
username = '2017302344'
password = '04045912'
book_url = 'http://10.81.0.88/book/book{}'


def find(d, s):
    return d.find_element_by_xpath(s)


def finds(d, s):
    return d.find_elements_by_xpath(s)


def login(d):
    d.implicitly_wait(2)
    d.get('http://10.81.0.88/index.php')
    try:
        d.find_element_by_id('username').send_keys(username)
        d.find_element_by_id('password').send_keys(password)
        find(d, '//*[@id="LoginForm"]/table/tbody/tr[3]/td[2]/input').click()
    except NoSuchElementException:
        pass
    d.implicitly_wait(10)


def get_bookID(s):
    return re.search('BookID=[0-9]+', s).group(0).split('=')[-1]


def for_book1(d):
    url = find(d, '//*[@id="c1_1"]//ul/li[1]//a').get_attribute('href')
    d.get(url)
    url_base = book_url.format(get_bookID(url)) + '/unit_index.php?UnitID={}'

    for unit in range(1, 11):
        url = url_base.format(str(unit))

        #=======================================================================
        # Listening
        d.get(url)
        #-----------------------------------------------------------------------
        # short conversations
        find(d, '//*[@id="toc"]/ul/li[1]/ul/li[1]/a').click()
        for i in range(10):
            # FIXME replace A with answer
            find(d, '//*[@value="A"]').click()
            find(d, '//*[@class="bottomButton"]/a[1]').click()
            # FIXME there may be an alter
            # d.switch_to.alert.accept()
            find(d, '//*[@class="bottomButton"]/a[2]').click()
        #-----------------------------------------------------------------------
        # long conversations
        for i in range(1, 6):
            # FIXME offset is answer, 1 for A, 2 for B, ...
            offset = 1
            find(d, '//*[@id="QuestionTBody"]/tr[{}]//*[@type="radio"]'\
                    .format((i - 1) * 5 + offset + 1)).click()
        find(d, '//*[@class="bottomButton"]/a[1]').click()
        # FIXME there may be an alter
        # d.switch_to.alert.accept()
        find(d, '//*[@class="bottomButton"]/a[2]').click()
        #-----------------------------------------------------------------------
        # passage
        for i in range(1, 6):
            # FIXME offset is answer, 1 for A, 2 for B, ...
            offset = 1
            find(d, '//*[@id="QuestionTBody"]/tr[{}]//*[@type="radio"]'\
                    .format((i - 1) * 5 + offset + 1)).click()
        find(d, '//*[@class="bottomButton"]/a[1]').click()
        # FIXME there may be an alter
        # d.switch_to.alert.accept()
        find(d, '//*[@class="bottomButton"]/a[2]').click()
        #-----------------------------------------------------------------------
        # radio program
        try:
            re.search('input type="radio"', d.page_source).group(0)
            for i in range(1, 6):
                # FIXME offset is answer, 1 for A, 2 for B, ...
                offset = 1
                find(d, '//*[@id="QuestionTBody"]/tr[{}]//*[@type="radio"]'\
                        .format((i - 1) * 5 + offset + 1)).click()
        except AttributeError:
            for i in finds(d, '//*[@id="QuestionForm"]/table/tbody/tr/td//input'):
                # FIXME replace "A" with answer
                i.send_keys('A')
        find(d, '//*[@class="bottomButton"]/a[1]').click()
        # FIXME there may be an alter
        # d.switch_to.alert.accept()
        #=======================================================================
        # homework
        d.get(url)
        #-----------------------------------------------------------------------
        # long conversations
        find(d, '//*[@id="toc"]/ul/li[4]/ul/li[1]/a').click()
        for i in range(1, 6):
            # FIXME offset is answer, 1 for A, 2 for B, ...
            offset = 1
            find(d, '//*[@id="QuestionTBody"]/tr[{}]//input'\
                    .format((i - 1) * 6 + offset + 1)).click()
        find(d, '//*[@class="bottomButton"]/a[1]').click()
        # FIXME there may be an alter
        # d.switch_to.alert.accept()
        find(d, '//*[@class="bottomButton"]/a[2]').click()
        #-----------------------------------------------------------------------
        # passage
        for i in range(1, 6):
            # FIXME offset is answer, 1 for A, 2 for B, ...
            offset = 1
            find(d, '//*[@id="QuestionTBody"]/tr[{}]//*[@type="radio"]'\
                    .format((i - 1) * 6 + offset + 1)).click()
        find(d, '//*[@class="bottomButton"]/a[1]').click()
        # FIXME there may be an alter
        # d.switch_to.alert.accept()
        find(d, '//*[@class="bottomButton"]/a[2]').click()
        #-----------------------------------------------------------------------
        # compound dictation
        for i in finds(d, '//*[@id="QuestionForm"]/table/tbody/tr/td//input'):
            # FIXME replace "A" with answer
            i.send_keys('A')
        find(d, '//*[@class="bottomButton"]/a[1]').click()
        # FIXME there may be an alter
        # d.switch_to.alert.accept()


def for_book2(d):
    url = find(d, '//*[@id="c1_1"]//ul/li[3]//a').get_attribute('href')
    d.get(url)
    url_base = book_url.format(get_bookID(url)) + '/app_index.php?unit={}'

    for i in range(8):
        url = url_base.format(i + 1)
        d.get(url)


if __name__ == '__main__':
    d = webdriver.Chrome()
    d.implicitly_wait(2)

    login(d)
    for_book1(d)
    # login(d)
    # for_book2(d)


