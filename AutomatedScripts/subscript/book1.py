#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import json


def get_bookID(s):
    return re.search('BookID=[0-9]+', s).group(0).split('=')[-1]


def find(d, s):
    return d.find_element_by_xpath(s)


def finds(d, s):
    return d.find_elements_by_xpath(s)


def go_next(d):
    find(d, '//*[@class="bottomButton"]/a[2]').click()


def submit(d):
    find(d, '//*[@class="bottomButton"]/a[1]').click()
    # TODO there may be an alter


def by_type(d, answer={'type': -1}):
    # multiple choice question
    if answer['type'] == 0:
        blk_num = 6
        for i in finds(d, '//*[@id="QuestionTBody"]/tr[6]//td'):
            if i.text.strip() != '':
                blk_num = 5
                break
        for i in range(1, 6):
            offset = {'A': 1, 'B': 2, 'C': 3, 'D': 4}[answer['answer'][i - 1]]
            find(d, '//*[@id="QuestionTBody"]/tr[{}]//*[@type="radio"]'\
                    .format((i - 1) * blk_num + offset + 1)).click()
        submit(d)
    # short conversations
    elif answer['type'] == 1:
        for i in range(10):
            find(d, '//*[@value="{}"]'.format(answer['answer'][i])).click()
            submit(d)
            go_next(d)
    # fill in the blanks
    elif answer['type'] == 2:
        cnt = 0
        for i in finds(d, '//*[@id="QuestionForm"]/table/tbody/tr/td//input'):
            i.send_keys(answer['answer'][cnt])
            cnt += 1
        submit(d)
    # no answer or skip


def run(d):
    # prepare
    url = find(d, '//*[@id="c1_1"]//ul/li[1]//a').get_attribute('href')
    d.get(url)
    bookID = get_bookID(url)

    book_url = 'http://10.81.0.88/book/book{}'
    url_base = book_url.format(bookID) + '/unit_index.php?UnitID={}'
    answer = json.load(open('answer/' + bookID + '.json'))

    for unit in range(1, 11):
        unit_answer = answer[str(unit)]
        url = url_base.format(str(unit))
        ### Listening
        d.get(url)
        # short conversations
        find(d, '//*[@id="toc"]/ul/li[1]/ul/li[1]/a').click()
        by_type(d, unit_answer['LSC'])
        # long conversations
        by_type(d, unit_answer['LLC'])
        go_next(d)
        # passage
        by_type(d, unit_answer['LPS'])
        go_next(d)
        # radio program
        by_type(d, unit_answer['LRP'])
        ### homework
        d.get(url)
        find(d, '//*[@id="toc"]/ul/li[4]/ul/li[1]/a').click()
        # long conversations
        by_type(d, unit_answer['HLC'])
        go_next(d)
        # passage
        by_type(d, unit_answer['HPS'])
        go_next(d)
        # compound dictation
        by_type(d, unit_answer['HCD'])

