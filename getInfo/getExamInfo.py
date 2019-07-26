#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从翱翔门户获取考试安排和考试成绩
"""
import os
import sys
import datetime
sys.path.append('..')
from bs4 import BeautifulSoup
from functions import AoxiangInfo

# FIXME 表格的ID似乎很奇怪，只能先每学期都改改了
#第一学期17,第二学期35,上学期18, 本学期为36
urlGrade = 'http://us.nwpu.edu.cn/eams/teach/grade/course/person!search.action?semesterId=36'
urlExam = 'http://us.nwpu.edu.cn/eams/stdExamTable!examTable.action?examBatch.id=382'
long_len, short_len = 22, 14
examExist = 1
#设置挂科显示debug状态(万一你是dalao无科可挂呢)
DEBUG = 0
#设置debug时成绩的修正值
debugValue = 30

help_msg = """
\033[32m-\033[m 带 * 的表示是实验课
"""


#计算字符串所占字符数
def charlen(string):
    jud = lambda x: u'\u4e00' <= x <= u'\u9fa6'
    length = 0
    for char in string: length += 2 if jud(char) else 1
    return length


def format_string(string, num, color=''):
    string = string.replace('实验', '*').strip()

    blk_n = num - charlen(string)
    ret = string if blk_n >= 0 else string[0:num//2-3] + '...'
    blk_n = num - charlen(ret)

    ret += '\033[m' + ' ' * blk_n
    ret = ret.replace('*', '\033[32m*\033[m')
    return color + ret


# 获取表格长度
def getTableLen():
    soupG = BeautifulSoup(AoxiangInfo.get(urlGrade), features='html5lib')
    colCntE = 7
    colCntG = len(soupG.find_all('th')[5:])

    # 用于计算表格长度,动态调整分割线
    global tableLength

    if colCntG > colCntE and examExist or examExist == 0:
        tableLength = long_len + short_len * (colCntG - 1) + 4
    else:
        tableLength = long_len + short_len * colCntE


# TODO 增加本学期平均分计算功能
def get_grade():
    """ 获取成绩信息 """
    soup = BeautifulSoup(AoxiangInfo.get(urlGrade), features='html5lib')

    # 最终,总评成绩,补考成绩的列号
    totalCol = makeUpCol = finalCol = -1
    # 学分,绩点的列号
    creditCol = GPCol = -1

    head = tableLength * '=' + '\n'
    line = format_string('', long_len)
    col = 0
    for th in soup.find_all('th')[5:]:
        line += format_string(th.string, short_len)

        if   th.string == "总评成绩":
            totalCol = col
        elif th.string == "补考成绩":
            makeUpCol = col
        # NOTE 翱翔成绩单此项名为"最终",不是"最终成绩"...
        elif th.string == "最终":
            finalCol = col
        elif th.string == "学分":
            creditCol = col
        elif th.string == "绩点":
            GPCol = col

        col += 1
    head += line + '\n' + tableLength * '-' + '\n'

    lines = []
    for tr in soup.find_all('tr')[1:]:
        try: line = tr.find_all('a')[0].string
        except IndexError: break

        line = format_string(line, long_len)
        scoreVal, cnt = 0, -1
        for td in tr.find_all('td')[5:]:
            cnt += 1
            text = str(td.string).lower()
            if text == 'none':
                line += format_string('-', short_len)
                continue

            try: scoreVal = float(td.string)
            except ValueError: scoreVal = -1

            if bool(DEBUG) and scoreVal != -1:
                scoreVal -= debugValue
                if cnt not in [creditCol, GPCol]:
                    td.string = '{:.1f}'.format(float(td.string) - debugValue)
                elif cnt == GPCol:
                    td.string = '{:.1f}'.format(float(td.string) - 2)

            score = td.string
            # 注意翱翔成绩单上显示P的成绩两边带空格...艹
            if td.string.strip() == "P":
                # 显示P的成绩认为是满分
                scoreVal = 100
            elif scoreVal == -1:
                score = score.replace('-','')
                score = score.replace(' ','')
                score = score.replace('（','')
                score = score.replace('）','')
                score = score.replace('(','')
                score = score.replace(')','')
                score = score.replace("申请","")

            color = '\033[31m' if \
                            cnt in [totalCol, makeUpCol, finalCol] and \
                            (scoreVal < 60 or scoreVal == -1) \
                    else ''
            line += format_string(score, short_len, color)
        lines.append(line.replace('（', '(').replace('）', ')').replace('：',':'))

    result = '\n'.join(sorted(lines)[::-1]) + '\n'

    return '' if result.strip() == '' else head + result + tableLength * '='


# TODO 期中考试的安排...
def get_exam():
    """ 考试安排 """
    soup = BeautifulSoup(AoxiangInfo.get(urlExam), features='html5lib')

    head = '\n' + tableLength * '=' + '\n'
    line = ''
    th = soup.find_all('th')
    index = [1, 2, 3, 4, 5, 7, 8, 9]
    for idx in index:
        if idx == 1: line += format_string('', long_len)
        else: line += format_string(th[idx].string, short_len)

    head += line + '\n' + tableLength * '-' + '\n'

    lines = []
    for tr in soup.find_all('tr')[1:]:
        line = ''
        td = tr.find_all('td')

        for idx in index:
            text = str(td[idx].string).lower()
            if text != 'none':
                line += format_string(td[idx].string if idx != 7 else td[idx].find_all('a')[0].string,
                                  short_len if idx != 1 else long_len)
            else: line += format_string('-', short_len)

        et = td[3].string.replace('-', '')
        et += td[4].string.split('~')[-1].replace(':', '')
        et = datetime.datetime(int(et[0:4]), int(et[4:6]), int(et[6:8]),\
                               int(et[8:10]), int(et[10:12]))
        if datetime.datetime.now() < et or bool(DEBUG):
            lines.append(line.replace('（', '(').replace('）', ')'))

    result = '\n'.join(sorted(lines)[::-1]) + '\n'

    return '' if result.strip() == '' else head + result


if __name__ == '__main__':
    getTableLen()
    examRes = get_exam()
    examExist = 0 if examRes == '' else 1
    getTableLen()

    os.system('')
    print(examRes)
    print(get_grade())
    print(help_msg)

