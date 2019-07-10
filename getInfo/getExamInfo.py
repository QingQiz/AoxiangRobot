#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从翱翔门户获取考试安排和考试成绩
"""
import sys
import datetime
sys.path.append('..')
from bs4 import BeautifulSoup
from functions import AoxiangInfo

# FIXME 表格的ID似乎很低怪，只能先每学期都改改了
urlGrade = 'http://us.nwpu.edu.cn/eams/teach/grade/course/person!search.action?semesterId=36'
urlExam = 'http://us.nwpu.edu.cn/eams/stdExamTable!examTable.action?examBatch.id=382'
debugValue = 30     #设置debug时成绩的修正值
DEBUG = False       #设置挂科显示debug状态(万一你是dalao无科可挂呢)

def format_string(string, num, color=''):
    string = string.strip()
    jud = lambda x: u'\u4e00' <= x <= u'\u9fa6'
    length = 0
    for char in string:
        length += 2 if jud(char) else 1
    res = num - length

    if(res >= 0):                                   #判断字符串长度
        ret = string
        ret += ' ' * res
    else:                                           #| 若超过设定长度
        ret = string[0:(num//2)-2]                  #| 则只取一部分
        ret += '... '                               #| 末尾加'...'
    return color + ret[0:len(string)] + '\033[0m' + ret[len(string):]


# 查成绩
# TODO 增加补考等情况的格式
# TODO 增加本学期平均分计算功能
def get_grade():
    soup = BeautifulSoup(AoxiangInfo.get(urlGrade), features='html5lib')
    long_len, short_len = 22, 12
    result = 107 * '=' + '\n'
    line = format_string('', long_len)
    for th in soup.find_all('th')[5:]:
        line += format_string(th.string, short_len)
    result += line + '\n' + 107 * '-' + '\n'

    for tr in soup.find_all('tr')[1:]:
        line = tr.find_all('a')[0].string
        line = format_string(line, long_len)

        total = cnt = 0
        for td in tr.find_all('td')[5:]:
            text = str(td.string).lower()
            if text != 'none':
                total = float(td.string)                        #总评成绩

                if DEBUG:                                       #|用于测试挂科样例
                    total -= debugValue
                    if cnt not in [0, 6]:
                        td.string = '{:.1f}'.format(float(td.string) - debugValue)
                    elif cnt == 6:
                        td.string = '{:.1f}'.format(float(td.string) - 2)

                score = format_string(td.string, short_len)
                if cnt in [4, 5] and total < 60:
                    score = format_string(td.string, short_len, '\033[1;37;41m')
                line += score
            else:
                line += format_string('-', short_len)
            cnt += 1
        result += line.replace('（', '(').replace('）', ')') + '\n'
    return result + 107 * '=' + '\n'


def get_exam():
    soup = BeautifulSoup(AoxiangInfo.get(urlExam), features='html5lib')
    long_len, short_len = 22, 15
    head = '\n' + 107 * '=' + '\n'
    result = line = ''
    th = soup.find_all('th')
    index = [1, 2, 3, 4, 5, 7, 8]
    for idx in index:
        line += format_string(th[idx].string if idx != 1 else '',
                              short_len if idx != 1 else long_len)
    head += line + '\n' + 107 * '-' + '\n'

    for tr in soup.find_all('tr')[1:]:
        line = ''
        td = tr.find_all('td')

        for idx in index:
            line += format_string(td[idx].string if idx != 7 else td[idx].find_all('a')[0].string,
                                  short_len if idx != 1 else long_len)
        et = td[3].string.replace('-', '')
        et += td[4].string.split('~')[-1].replace(':', '')
        et = datetime.datetime(int(et[0:4]), int(et[4:6]), int(et[6:8]),\
                               int(et[8:10]), int(et[10:12]))
        if datetime.datetime.now() < et:
            result += line.replace('（', '(').replace('）', ')') + '\n'
    if result == '':
        return ''
    return head + result


print(get_exam())
print(get_grade())

