#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from . import AoxiangInfo

urlExam = """
http://us.nwpu.edu.cn/eams/stdExamTable!examTable.action?examBatch.id=
"""

header = {
    "name": "",
    "type": "考试类型",
    "date": "考试日期",
    "time": "考试时间",
    "campus": "考场校区",
    "room": "考场教室",
    "status": "考试情况",
    "description": "其它说明"
}


def get(*args):
    res = []
    for Id in args:
        url = urlExam.strip() + str(Id)
        soup = BeautifulSoup(AoxiangInfo.get(url), features='html5lib')

        dic = {
            "name": 1,
            "type": 2,
            "date": 3,
            "time": 4,
            "campus": 5,
            "room": 7,
            "status": 8,
            "description": 9
        }

        result = []
        for tr in soup.find_all('tr')[1:]:
            tds = tr.find_all('td')

            def content(idx):
                res = tds[idx].find_all('a')[0].string if idx == 7 else tds[idx].string
                return None if res is None else res.strip()

            try:
                result.append({key: content(dic[key]) for key in dic})
            except IndexError:
                break
        res.append(result)
    return res

