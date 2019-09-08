#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import datetime
from lxml import etree
from .. import AoxiangInfo
from . import GetSettings


def get_time_table(class_time=None):
    if class_time is None:
        time_table_js = GetSettings.get_default_time_settings()
    else:
        time_table_js = class_time
    time_table = [{}]
    for i in time_table_js:
        try:
            time_start = i.get('time').get('start')
        except AttributeError:
            time_start = None
        if time_start is None:
            time_start = time_table[-1].get('end')
            time_start = datetime.datetime(1, 1, 1, int(time_start[0:2]), int(time_start[2:4]), 0)
            time_start += datetime.timedelta(minutes=int(i.get('offset')))
        else:
            time_start = datetime.datetime(1, 1, 1, int(time_start[0:2]), int(time_start[2:4]), 0)
        time_end = time_start + datetime.timedelta(minutes=int(i.get('during')))

        time_table.append({
            "name": i.get('name'),
            "start": format(str(time_start.hour), '0>2') + format(time_start.minute, '0>2'),
            "end": format(str(time_end.hour), '0>2') + format(time_end.minute, '0>2'),
        })
    res = {}
    for i in time_table[1:]:
        res[i.get('name')] = {'start': i.get('start'), 'end': i.get('end')}
    return res


def get(class_time=None):
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

    time_table = get_time_table(class_time)

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
                        "start": time_table[time[0]].get('start'),
                        "end": time_table[time[1]].get('end'),
                    },
                    "room": infoList[-1],
                    "teacher": teacher,
                })
    return res
