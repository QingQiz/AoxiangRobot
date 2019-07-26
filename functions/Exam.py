#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('..')
from bs4 import BeautifulSoup
from functions import AoxiangInfo

urlExam = """
http://us.nwpu.edu.cn/eams/stdExamTable!examTable.action?examBatch.id=
"""


def get(Id=382):
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

        result.append({key: content(dic[key]) for key in dic})

    return result

