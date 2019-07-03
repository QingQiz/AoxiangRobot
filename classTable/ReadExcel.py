#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd
import copy
import json

rt_dir = 'settings'

class_info = xlrd.open_workbook(rt_dir + '/classInfo.xlsx')
class_time = xlrd.open_workbook(rt_dir + '/ClassTimeSetting.xlsx')

table = class_info.sheets()[0]
dic = {}

for i in range(table.ncols):
    dic[table.cell(0, i).value] = copy.deepcopy([])
    for j in range(1, table.nrows):
        dic[table.cell(0, i).value].append(table.cell(j, i).value)

res = []
for i in range(len(dic.get('name'))):
    res.append({
        'name': str(dic['name'][i]),
        'week': {
            'start': str(int(dic['startweek'][i])),
            'end': str(int(dic['endweek'][i])),
        },
        'day': str(int(dic['weekday'][i])),
        'time': {
            'start': str(int(dic['starttime'][i])),
            'end': str(int(dic['endtime'][i])),
        },
        'room': str(dic['room'][i]),
    })

with open(rt_dir + '/classInfo.json', 'w') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)


table = class_time.sheets()[0]
dic = {}

for i in range(table.ncols):
    dic[table.cell(0, i).value] = copy.deepcopy([])
    for j in range(1, table.nrows):
        dic[table.cell(0, i).value].append(table.cell(j, i).value)

res = []

for i in range(len(dic.get('name'))):
    part = {
        'name': str(int(dic['name'][i])),
    }
    if dic['during'][i] != '':
        part['during'] = str(int(dic['during'][i]))
    if dic['timestart'][i] != '':
        part['time'] = {
            'start': format(str(int(dic['timestart'][i])), '0>4'),
        }
    if dic['offset'][i] != '':
        part['offset'] = str(int(dic['offset'][i]))
    res.append(part)


with open(rt_dir + '/ClassTimeSetting.json', 'w') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)

