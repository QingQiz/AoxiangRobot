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
debugValue = 30
DEBUG = False

def format_string(string, num):
    string = string.strip()
    jud = lambda x: u'\u4e00' <= x <= u'\u9fa6'
    length = 0
    for char in string:
        length += 2 if jud(char) else 1
    res = num - length

    if(res >= 0):                                   #判断字符串长度
        ret = string
        #for i in range(res):
        ret += ' ' * res
    else:                                           #| 若超过设定长度
        ret = string[0:(num//2)-2]                  #| 则只取一部分
        ret += '... '                               #| 末尾加'...'
    return ret


def setWarning(string, isFail):                     #红色显示挂科
    if(isFail):
        result = '\033[5;37;41m' + string + '\033[0m' + '\033[5;37;41mgk++\033[0m' + '\n'
    else:
        result = string + '\n'
    return result

def get_grade():                                    #查成绩    TODO: 增加补考等情况的格式
    soup = BeautifulSoup(AoxiangInfo.get(urlGrade), features='html5lib')
    long_len, short_len = 20, 12                    #long_len由22改为20
    result = ''
    line = format_string('', long_len)
    for th in soup.find_all('th')[5:]:
        line += format_string(th.string, short_len)
    result += line + '\n' + 107 * '-' + '\n'        #添加了分割线'---'
    for tr in soup.find_all('tr')[1:]:
        line = tr.find_all('a')[0].string
        line = format_string(line, long_len)
        fail = 0

        for td in tr.find_all('td')[5:]:
            text = str(td.string).lower()
            if(text != 'none'):
                total = float(tr.find_all('td')[8].string)                      #总评成绩

                if(DEBUG):                                                      #|用于测试挂科样例
                    total -=debugValue                                          #|
                    if(td in tr.find_all('td')[6:10]):                          #|
                        td.string = '{:.1f}'.format(float(td.string)-debugValue)#|
                    elif(td is tr.find_all('td')[10]):                          #|
                        td.string = '{:.1f}'.format(float(td.string)-2)         #|

                score = format_string(td.string, short_len)                     #| 各项成绩
                if((total < 60) and (td is tr.find_all('td')[8])):              #| 如果总评成绩<60
                    fail = 1                                                    #| 设置为挂科
                    #score=setWarning(score,fail)
                    
                line += score

            else:
                line += format_string('-', short_len)

        item = line.replace('（', '(').replace('）', ')')
        result += setWarning(item, fail)
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
    result += line + '\n' + 107 * '-' + '\n'        #添加了分割线'---'

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

