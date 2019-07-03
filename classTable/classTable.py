#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import time
import datetime
import random

js = json.load(open('settings/classInfo.json'))
time_table_js = json.load(open('settings/ClassTimeSetting.json'))
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



head = open('material/HEAD').read().strip('\n')
body = []
body_template = open('material/BODY').read().strip('\n')
tail = open('material/TAIL').read().strip('\n')


def uid():
    choice = 'qazwsxedcrfvtgbyhnujmikolp'
    choice += choice.upper()
    res = ''
    for i in range(20):
        res += random.choice(choice)
    return res


def format_template(name, tstart, tend, room, alarm):
    timeNow = time.strftime("%Y%m%dT%H%M%SZ", time.localtime())
    body_elem = body_template.format(created=timeNow, uid1=uid(), uid2=uid(), uid3=uid(), tend=tend, tstart=tstart,
                                     room=room, alarm=alarm, name=name)
    return body_elem


def format_date(date, time):
    f = lambda x: format(str(x), '0>2')
    return f(date.year) + f(date.month) + f(date.day) + 'T' + time + '00'


def get_time(d):
    start = d.get('start')
    end = d.get('end')
    return time_table[int(start)].get('start'), time_table[int(end)].get('end')


if __name__ == '__main__':
    try:
        term_start = input('The date of Monday of the first week of school(20190826):________\b\b\b\b\b\b\b\b')
    except KeyboardInterrupt:
        print('\ninterrupted. exiting...')
        exit(0)
    if term_start == '':
        term_start = '20190826'
    try:
        y = int(term_start[0:4])
        m = int(term_start[4:6])
        d = int(term_start[6:8])
        term_start = datetime.datetime(y, m, d)
        if term_start.weekday() != 0:
            raise ValueError
    except (ValueError, IndexError):
        print('invalid input')
        exit(-1)

    dic = {}
    for i in js:
        dic[str(i)] = uid()
    for i in dic:
        c = json.loads(i.replace("'", '"'), encoding='utf8')

        start_time, end_time = get_time(c.get('time'))

        c_week_start, c_week_end = int(c.get('week').get('start')), int(c.get('week').get('end'))

        for j in range(c_week_start, c_week_end + 1):
            date = term_start + datetime.timedelta(days=((j-1)*7+int(c.get('day'))-1))
            tstart, tend = format_date(date, start_time), format_date(date, end_time)
            body.append(format_template(c.get('name'), tstart, tend, c.get('room'), '20'))

    with open('res.ics', 'w') as f:
        f.write(head)
        f.write('\n')
        for i in body:
            f.write(i)
            f.write('\n')
        f.write(tail)

