#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import json
from lxml import etree
sys.path.append('..')
from functions import AoxiangInfo

ids = AoxiangInfo.get('http://us.nwpu.edu.cn/eams/courseTableForStd.action')
ids = re.search('"ids","[0-9]+"', ids).group(0).split('"')[3]

info = AoxiangInfo.post('http://us.nwpu.edu.cn/eams/courseTableForStd!courseTable.action', data={
       'ignoreHead': 1,
       'startWeek': 1,
       'semester.id': 19,
       'setting.kind': 'std',
       'project.id': 1,
       'ids': ids
   }
)
dic = {
    "星期一": "1",
    "星期二": "2",
    "星期三": "3",
    "星期四": "4",
    "星期五": "5",
    "星期六": "6",
    "星期日": "7",
}

xpath = '/html/body/div/table/tbody'
dom = etree.HTML(info, etree.HTMLParser())
trs = len(dom.xpath(xpath + '/tr'))
#       课程名称 安排 起止周 教师
infoIndex = [4, 8, 9, 5]

res = []
for i in range(trs):
    data = lambda y: \
        dom.xpath(xpath + '/tr[{}]/td[{}]//text()'.format(i + 1, infoIndex[y]))[0].strip()

    if data(3) == '在线开放课程':
        continue
    for c in dom.xpath(xpath + '/tr[{}]/td[{}]//text()'.format(i + 1, infoIndex[1])):
        teacher = data(3)
        c = c[c.find('星期'):].strip()
        name = data(0)

        infoList = c.split(' ')
        for j in infoList[2].split(','):
            time = infoList[1].split('-')
            week = j.replace('[', '').replace(']', '').split('-')

            res.append({
                "name": name,
                "week": {
                    "start": week[0],
                    "end": week[-1]
                },
                "day": dic[infoList[0]],
                "time": {
                    "start": time[0],
                    "end": time[1],
                },
                "room": infoList[3]
            })

with open('settings/classInfo.json', 'w', encoding='utf8') as f:
    json.dump(res, f, indent=4, ensure_ascii=False)
