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

# FIXME Windows貌似显示彩色字符串会出错...
# FIXME 表格的ID似乎很奇怪，只能先每学期都改改了
urlGrade = 'http://us.nwpu.edu.cn/eams/teach/grade/course/person!search.action?semesterId=36' #第一学期17,第二学期35,上学期18, 本学期为36
urlExam = 'http://us.nwpu.edu.cn/eams/stdExamTable!examTable.action?examBatch.id=382'
long_len, short_len = 22, 14
global examExist    #标记是否有排考信息输出
examExist = 1

debugValue = 30     #设置debug时成绩的修正值
DEBUG = False       #设置挂科显示debug状态(万一你是dalao无科可挂呢)

#计算字符串所占字符数
def charlen(string):
    jud = lambda x: u'\u4e00' <= x <= u'\u9fa6'
    length = 0
    for char in string:
        length += 2 if jud(char) else 1
    return length

def format_string(string, num, color=''):
    string = string.strip()
    res = num - charlen(string)

    if(res >= 0):                                   #判断字符串长度
        ret = string
    else:                                           #| 若超过设定长度
        ret = string[0:(num//2)-3]                  #| 则只取一部分(zh)
        ret += '...'                                #| 末尾加'...'
        res = num - charlen(ret)
    if color != '':
        res += 4                                    #带颜色的字符格式化时貌似会多计算4个字符,补偿空格
        
    ret += ' ' * res                                #加空格对齐
    return color + ret[0:len(string)] + '\033[0m' + ret[len(string):]

# 获取表格长度
def getTableLen():
    soupG = BeautifulSoup(AoxiangInfo.get(urlGrade), features='html5lib')
    colCntG = 0
    colCntE = 7
    for th in soupG.find_all('th')[5:]:
        colCntG += 1

    global tableLength                              #用于计算表格长度,动态调整分割线
    if colCntG > colCntE and examExist or examExist == 0:
        tableLength = long_len + short_len * (colCntG - 1) + 4
    else:
        tableLength = long_len + short_len * colCntE

# 查成绩
# TODO 增加本学期平均分计算功能
def get_grade():
    soup = BeautifulSoup(AoxiangInfo.get(urlGrade), features='html5lib')
    
    totalCol = makeUpCol = finalCol = -1            #| 最终,总评成绩,补考成绩的列号
    creditCol = GPCol = -1                          #| 学分,绩点的列号
                                                    #| 若无此项则列号为-1
    head = tableLength * '=' + '\n'
    line = format_string('', long_len)
    col = 0
    for th in soup.find_all('th')[5:]:
        line += format_string(th.string, short_len)

        if   th.string == "总评成绩":
            totalCol = col
        elif th.string == "补考成绩":
            makeUpCol = col
        elif th.string == "最终":     #注意翱翔成绩单此项名为"最终",不是"最终成绩"...
            finalCol = col
        elif th.string == "学分":
            creditCol = col
        elif th.string == "绩点":
            GPCol = col

        col += 1
    head += line + '\n' + tableLength * '-' + '\n'

    result = ''
    for tr in soup.find_all('tr')[1:]:
        try:
            line = tr.find_all('a')[0].string
        except IndexError:
            break

        line = format_string(line, long_len)
        scoreVal = cnt = 0
        for td in tr.find_all('td')[5:]:
            text = str(td.string).lower()
            if text != 'none':
                try:
                    scoreVal = float(td.string)                     #成绩数值
                except ValueError:
                    scoreVal = -1                                   #缓考,缺考等表格内容为文字的情况

                if DEBUG and scoreVal != -1:                        #用于测试挂科样例
                    scoreVal -= debugValue
                    if cnt not in [creditCol, GPCol]:
                        td.string = '{:.1f}'.format(float(td.string) - debugValue)
                    elif cnt == GPCol:
                        td.string = '{:.1f}'.format(float(td.string) - 2)

                score = format_string(td.string, short_len)
                if td.string.strip() == "P":                        #注意翱翔成绩单上显示P的成绩两边带空格...艹
                    scoreVal = 100                                  #显示P的成绩认为是满分
                elif scoreVal == -1:
                    score = score.replace('-','')                   #删去翱翔上面啰哩啰嗦的废话
                    score = score.replace(' ','')
                    score = score.replace('（','')
                    score = score.replace('）','')
                    score = score.replace('(','')
                    score = score.replace(')','')
                    score = score.replace("申请","")
                    
                if cnt in [totalCol, makeUpCol, finalCol] and scoreVal < 60 or scoreVal == -1:
                    score = format_string(score, short_len, '\033[1;37;41m')    #异常情况显示为红色高亮
                line += score
            else:
                line += format_string('-', short_len)
            cnt += 1
        result += line.replace('（', '(').replace('）', ')').replace('：',':') + '\n'
    if result == '':
        return ''
    return head + result + tableLength * '=' + '\n'


def get_exam():
    soup = BeautifulSoup(AoxiangInfo.get(urlExam), features='html5lib')
    
    head = '\n' + tableLength * '=' + '\n'
    result = line = ''
    th = soup.find_all('th')
    index = [1, 2, 3, 4, 5, 7, 8, 9]
    for idx in index:
        line += format_string(th[idx].string if idx != 1 else '',
                              short_len if idx != 1 else long_len)
        
    head += line + '\n' + tableLength * '-' + '\n'

    for tr in soup.find_all('tr')[1:]:
        line = ''
        td = tr.find_all('td')

        for idx in index:
            text = str(td[idx].string).lower()
            if text != 'none':
                line += format_string(td[idx].string if idx != 7 else td[idx].find_all('a')[0].string,
                                  short_len if idx != 1 else long_len)
            else:
                line += format_string('-', short_len)

        et = td[3].string.replace('-', '')
        et += td[4].string.split('~')[-1].replace(':', '')
        et = datetime.datetime(int(et[0:4]), int(et[4:6]), int(et[6:8]),\
                               int(et[8:10]), int(et[10:12]))
        if datetime.datetime.now() < et or DEBUG:
            result += line.replace('（', '(').replace('）', ')') + '\n'
    if result == '':
        examExist = 0
        return ''
    return head + result

getTableLen()
examRes = get_exam()
examExist = 0 if examRes == '' else 1
getTableLen()       #如果无排考信息输出,表格长度可能会变短

print(examRes)
print(get_grade())