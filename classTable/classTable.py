#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import datetime
import random
import GetClass


def get_data(js, term_start):
    def get_start_time(term_start=''):
        if term_start == '':
            term_start = '20190826'
        try:
            y = int(term_start[0:4])
            m = int(term_start[4:6])
            d = int(term_start[6:8])
            res = datetime.datetime(y, m, d)
            if res.weekday() != 0:
                raise ValueError
        except (ValueError, IndexError):
            print('invalid input')
            exit(-1)
        return res


    def format_date(date, time):
        f = lambda x: format(str(x), '0>2')
        return f(date.year) + f(date.month) + f(date.day) + 'T' + time + '00'


    term_start = get_start_time(term_start)
    for c in js:
        start_time, end_time = c.get('time').get('start'), c.get('time').get('end')

        step = 1
        c_week_start = int(c.get('week').get('start'))
        c_week_end = c.get('week').get('end')
        try:
            c_week_end = int(c_week_end)
        except ValueError:
            step = 2
            if c_week_end[-1] == '单':
                c_week_start = c_week_start | 1
            elif c_week_end[-1] == '双':
                c_week_start += c_week_start & 1
            else:
                raise ValueError
            c_week_end = int(c_week_end[:-1])

        for j in range(c_week_start, c_week_end + 1, step):
            date = term_start + datetime.timedelta(days=((j-1)*7+int(c.get('day'))-1))
            tstart, tend = format_date(date, start_time), format_date(date, end_time)
            data = {
                "name": c.get('name'),
                'tstart':  tstart,
                'tend': tend,
                'room': c.get('room'),
                'alarm': '20',
                'mdes': 'Teacher: ' + c.get('teacher'),
                'ades': ''
            }
            yield data


def get_json(term_start):
    js = GetClass.get()
    res = []
    for data in get_data(js, term_start):
        res.append({
            "title": data['name'],
            'description': 'ClassRoom: {}\n'.format(data['room']) + data['mdes'],
            'start': data['tstart'],
            'end': data['tend'],
        })
    return res


def get_calendar(term_start):
    def uid():
        choice = 'qazwsxedcrfvtgbyhnujmikolp'
        choice += choice.upper()
        return ''.join([random.choice(choice) for i in range(20)])


    def format_template(name, tstart, tend, room, alarm, mdes='', ades=''):
        timeNow = time.strftime("%Y%m%dT%H%M%SZ", time.localtime())
        body_elem = body_template.format(created=timeNow, uid1=uid(), uid2=uid(), uid3=uid(), tend=tend, tstart=tstart,
                                         room=room, alarm=alarm, name=name, mdes=mdes, ades=ades)
        return body_elem


    js = json.load(open('settings/classInfo.json', encoding='utf8'))
    head = open('material/HEAD', encoding='utf8').read().strip('\n').format(datetime.datetime.now().timestamp())
    body = []
    body_template = open('material/BODY', encoding='utf8').read().strip('\n')
    tail = open('material/TAIL', encoding='utf8').read().strip('\n')

    for data in get_data(js, term_start):
        body.append(format_template(**data))

    return head + '\n{}\n'.format('\n'.join(body)) + tail


if __name__ == '__main__':
    try:
        term_start = input('The date of Monday of the first week of school(20190826):________\b\b\b\b\b\b\b\b')
    except KeyboardInterrupt:
        print('\ninterrupted. exiting...')
        exit(0)

    with open('res.ics', 'w', encoding='utf8') as f:
        f.write(get_calendar(term_start))

