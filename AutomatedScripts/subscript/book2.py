#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json


def find(d, s):
    return d.find_element_by_xpath(s)


def finds(d, s):
    return d.find_elements_by_xpath(s)


def get_bookID(s):
    return re.search('BookID=[0-9]+', s).group(0).split('=')[-1]


def go_next(d):
    find(d, '//*[@id="unipus"]/header/div/a/div').click()


def submit(d):
    find(d, '//*[@id="unipus"]/div/div[3]/div[2]/input').click()
    # XXX can be faster when there is no need an acception
    try:
        find(d, '//*[@id="unipus"]/div/div[3]/div[2]/div/div[2]/input[1]').click()
    except:
        pass


def by_type(d, answer={'type': -1}):
    # choose from severl boxes
    if answer['type'] == 0:
        for i in answer['answer']:
            find(d, '//*[@id="unipus"]/div/div[3]/div[1]/div/\
                    div[2]/div/ul/li[{}]'.format(i)).click()
        submit(d)
    # multiple choice question
    elif answer['type'] == 1:
        cnt = 1
        for i in answer['answer']:
            find(d, '//*[@id="unipus"]/div/div[3]/div[2]/div/div/ul/li[{}]\
                    //*[@value="{}"]'.format(cnt, i)).click()
            cnt += 1
        submit(d)
    # fill in the blanks
    elif answer['type'] == 2:
        cnt = 0
        for i in finds(d, '//*[@id="unipus"]/div/div[3]/div[1]/div/div[2]/div/ul\
                //input'):
            i.send_keys(answer['answer'][cnt])
            cnt += 1
        submit(d)
    # drag and sort
    elif answer['type'] == 3:
        pass
    # switch from a table
    elif answer['type'] == 4:
        pass
    # fill in the blanks in a table
    # text area
    elif answer['type'] == 5:
        pass
    # no answer or skip


def run(d):
    url = find(d, '//*[@id="c1_1"]//ul/li[3]//a').get_attribute('href')
    d.get(url)
    bookID = get_bookID(url)

    book_url = 'http://10.81.0.88/book/book{}'
    url_base = book_url.format(get_bookID(url)) + '/app_index.php?unit={}'
    answer = json.load(open('answer/' + bookID + '.json'))

    for unit in range(1, 9):
        url = url_base.format(unit)
        d.get(url)
        # outside view
        path = '//*[@id="unipus"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/\
                ul/li[1]/a'
        d.get(find(d, path).get_attribute('href'))


