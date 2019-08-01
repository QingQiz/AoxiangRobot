#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('..')
from bs4 import BeautifulSoup
from functions import AoxiangInfo, format_string

urlGrade = """
http://us.nwpu.edu.cn/eams/teach/grade/course/person!search.action?semesterId=
"""

header = {
    "name": "",
    "credit": "学分",
    "usual": "平时成绩",
    "midTerm": "期中成绩",
    "experimental": "实验成绩",
    "endTerm": "期末成绩",
    "makeUp": "补考成绩",
    "total": "总评成绩",
    "final": "最终",
    "GP": "绩点",
}


def get(*args, username=None, password=None):
    res = []
    for Id in args:
        url = urlGrade.strip() + str(Id)
        soup = BeautifulSoup(AoxiangInfo.get(url, username=username, password=password), features='html5lib')

        # 学分       平时         期中         实验              期末
        creditCol = usualCol = midTermCol = experimentalCol = endTermCol = -1
        # 总评       最终         补考         绩点
        totalCol = finalCol = makeUpCol = GPCol = -1
        nameCol = 3

        col = 0
        for th in soup.find_all('th'):
            if th.string == "学分":
                creditCol = col
            elif th.string == "平时成绩":
                usualCol = col
            elif th.string == "期中成绩":
                midTermCol = col
            elif th.string == "实验成绩":
                experimentalCol = col
            elif th.string == "期末成绩":
                endTermCol = col
            elif th.string == "总评成绩":
                totalCol = col
            elif th.string == "最终":
                finalCol = col
            elif th.string == "绩点":
                GPCol = col
            elif th.string == "补考成绩":
                makeUpCol = col
            col += 1

        dic = {
            "name": nameCol,
            "credit": creditCol,
            "usual": usualCol,
            "midTerm": midTermCol,
            "experimental": experimentalCol,
            "endTerm": endTermCol,
            "makeUp": makeUpCol,
            "total": totalCol,
            "final": finalCol,
            "GP": GPCol,
        }

        result = []
        for tr in soup.find_all('tr')[1:]:
            tds = tr.find_all('td')

            def content(idx):
                if idx == nameCol:
                    return tr.find_all('a')[0].string.strip()
                ret = None if idx == -1 else tds[idx].string
                if idx != 'name':
                    ret = format_string.remove_chars(ret, "申请", '(', ')', '（', '）', '--', ' ')
                else:
                    ret = format_string.replace_chars(ret, **{'（': '(', '）': ')'})
                return ret if ret is None else ret.strip()

            try:
                result.append({key: content(dic[key]) for key in dic})
            except IndexError:
                break
        res.append(result)

    score = credit = 0
    temp_list = []
    for i in res: temp_list += i
    for obj in temp_list:
        try:
            score += float(obj['final']) * float(obj['credit'])
            credit += float(obj['credit'])
        except ValueError:
            pass
    return res, score / credit if credit != 0 else None
