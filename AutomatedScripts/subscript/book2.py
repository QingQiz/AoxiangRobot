#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *


def find(d, s):
    return d.find_element_by_xpath(s)


def finds(d, s):
    return d.find_elements_by_xpath(s)


def get_bookID(s):
    return re.search('BookID=[0-9]+', s).group(0).split('=')[-1]


def go_next(d):
    find(d, '//*[@id="unipus"]/header/div/a/div').click()


def submit(d):
    # submit
    find(d, '//*[@class="submit"]').click()
    # alter switch yes
    if find(d, '//*[@class="submit"]').get_attribute('id') != 'answer':
        find(d, '//*[@value="Yes"]').click()


def by_type_do(d, answer):
    # choose from severl boxes
    if answer['type'] == 0:
        sleep(0.5)
        for i in answer['answer']:
            find(d, '//*[@id="unipus"]/div//*[@value="{}"]'.format(i)).click()
            sleep(0.08)
        submit(d)
    # multiple choice question
    elif answer['type'] == 1:
        cnt = 0
        all_opitions = finds(d, '//*[@type="radio"]')
        for i in answer['answer']:
            if i not in '0123456789':
                offset = {'A': 1, 'B': 2, 'C': 3, 'D': 4}[i]
            else:
                offset = int(i)
            all_opitions[cnt * 4 + offset - 1].click()
            cnt += 1
        submit(d)
    # fill in the blanks
    elif answer['type'] == 2:
        cnt = 0
        for i in finds(d, '//*[@id="unipus"]/div//*[@type="text"]'):
            i.send_keys(answer['answer'][cnt])
            cnt += 1
        submit(d)
    # drag and sort
    elif answer['type'] == 3:
        dv = lambda v: \
                '//*[@id="unipus"]/div/div[3]//*[@data-value="{}"]'.format(v)
        action = ActionChains(d)

        pre = 'A'
        for now in reversed(answer['answer']):
            if now in '123456789':
                now = 'ABCDEFGHI'[int(now) - 1]
            action.drag_and_drop(find(d, dv(now)), find(d, dv(pre)))
            pre = now
        action.perform()
        submit(d)
    # fill in the blanks at a table
    elif answer['type'] == 4:
        rt_path = '//*[@id="unipus"]/div/div[3]/div[2]/div/div/table/tbody'
        width = len(finds(d, rt_path + '/tr[1]/td'))
        high = len(finds(d, rt_path + '/tr/td[1]'))
        cnt = 0
        for i in range(width):
            for j in range(high):
                path = rt_path + '/tr[{}]/td[{}]'.format(j + 1, i + 1)
                item = find(d, path)
                if len(re.findall('\(\d\)', item.text)) != 0:
                    find(d, path + '//input').send_keys(answer['answer'][cnt])
                    cnt += 1
        submit(d)
    # text area
    elif answer['type'] == 5:
        cnt = 0
        textarea = finds(d, '//*[@id="unipus"]//textarea')
        for i in answer['answer']:
            textarea[cnt].send_keys(i)
            cnt += 1
        submit(d)
    # select menu
    elif answer['type'] == 6:
        cnt = 0
        for i in finds(d, '//*[@id="unipus"]/div//select'):
            Select(i).select_by_value(answer['answer'][cnt])
            cnt += 1
        submit(d)
    # no answer or skip


def by_type(d, answer):
    try:
        by_type_do(d, answer)
    except ElementClickInterceptedException:
        sleep(1)
        by_type_do(d, answer)


def check_url(url):
    return re.search('S\d_\d$', url).group(0).split('_')[0].split('S')[-1]


def run(d):
    url = None
    for i in finds(d, '//*[@id="c1_1"]//ul/li[*]//a'):
        if len(re.findall('新标准大学英语（第二版）视听说', i.text)) != 0:
            url = i.get_attribute('href')
            break
    if url is None:
        return

    d.get(url)
    bookID = get_bookID(url)

    book_url = 'http://10.81.0.88/book/book{}'
    url_base = book_url.format(get_bookID(url)) + '/app_index.php?unit={}'
    answer = json.load(open('answer/' + bookID + '.json'))

    for unit in range(1, 9):
        unit_answer = answer[str(unit)]
        url = url_base.format(unit)

        ## outside view
        d.get(url)
        path = '//*[@id="unipus"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/\
                ul/li[1]/a'
        d.get(find(d, path).get_attribute('href'))
        ov_answer = unit_answer['OV']
        for i in ov_answer:
            by_type(d, ov_answer[i])
            go_next(d)
        while str(check_url(d.current_url)) == '2':
            go_next(d)

        ## Listening
        ls_answer = unit_answer['LS']
        for i in ls_answer:
            by_type(d, ls_answer[i])
            go_next(d)
        while str(check_url(d.current_url)) == '3':
            go_next(d)
        ## Unit test
        d.get(url)
        find(d, '//*[@href="#!/S6_1"]').click()
        ut_answer = unit_answer['UT']
        by_type(d, ut_answer)

