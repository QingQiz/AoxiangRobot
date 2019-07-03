#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从翱翔门户获取考试安排和考试成绩
"""
import sys
sys.path.append('..')
from bs4 import BeautifulSoup
from functions import AoxiangInfo

urlGrade = 'http://us.nwpu.edu.cn/eams/teach/grade/course/person!search.action?semesterId=36'
urlExam = 'http://us.nwpu.edu.cn/eams/stdExamTable!examTable.action?examBatch.id=382'


def format_string(string, num):
    string = string.strip()
    jud = lambda x: u'\u4e00' <= x <= u'\u9fa6'
    length = 0
    for char in string:
        length += 2 if jud(char) else 1
    res = num - length
    ret = string
    for i in range(res):
        ret += ' '
    return ret


def get_grade():
    soup = BeautifulSoup(AoxiangInfo.get(urlGrade), features='html5lib')
    long_len, short_len = 22, 10
    result = ''
    line = format_string('', long_len)
    for th in soup.find_all('th')[5:]:
        line += format_string(th.string, short_len)
    result += line + '\n'
    for tr in soup.find_all('tr')[1:]:
        line = tr.find_all('a')[0].string
        line = format_string(line, long_len)
        for td in tr.find_all('td')[5:]:
            text = str(td.string).lower()
            line += format_string(td.string, short_len) if text != 'none' else format_string('-', short_len)
        result += line.replace('（', '(').replace('）', ')') + '\n'
    return result


def get_exam():
    soup = BeautifulSoup(AoxiangInfo.get(urlExam), features='html5lib')
    long_len, short_len = 22, 15
    result = ''
    line = ''
    th = soup.find_all('th')
    index = [1, 2, 3, 4, 5, 7, 8]
    for idx in index:
        line += format_string(th[idx].string if idx != 1 else '',
                              short_len if idx != 1 else long_len)
    result += line + '\n'

    for tr in soup.find_all('tr')[1:]:
        line = ''
        td = tr.find_all('td')
        for idx in index:
            line += format_string(td[idx].string if idx != 7 else td[idx].find_all('a')[0].string,
                                  short_len if idx != 1 else long_len)
        result += line.replace('（', '(').replace('）', ')') + '\n'
    return result


print('\n' + 107 * '=' + '\n')
print(get_exam())
print(107 * '=' + '\n')
print(get_grade())
print(107 * '=' + '\n')

