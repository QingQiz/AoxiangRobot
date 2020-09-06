#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import string
import datetime
import random

from . import GetSettings


def get_data(js, term_start, method=None):
    """
    :param method: method for calculating time, 0 and None do nothing and 1 for Youyi Campus time schedule
    :param js: class info (json)
    :param term_start: first monday (20190826)
    :return:
    """

    def get_start_time(ts=''):
        if ts == '':
            ts = '20190826'
        try:
            y = int(ts[0:4])
            m = int(ts[4:6])
            d = int(ts[6:8])
            res = datetime.datetime(y, m, d)
            if res.weekday() != 0:
                raise ValueError
        except (ValueError, IndexError):
            print('invalid input')
            return
        return res

    def format_date(date, time, method):
        f = lambda x: format(str(x), '0>2')
        if method not in (None, 0, 1):
            raise ValueError
        if method is None or method == 0:
            return f(date.year) + f(date.month) + f(date.day) + 'T' + time + '00'
        else:
            dt = datetime.datetime(date.year, date.month, date.day, int(time[:2]), int(time[2:]))
            if datetime.datetime(dt.year, 5, 1) <= dt < datetime.datetime(dt.year, 10, 1):
                if dt >= datetime.datetime(dt.year, dt.month, dt.day, 14):
                    dt = dt + datetime.timedelta(minutes=30)
                return f(dt.year) + f(dt.month) + f(dt.day) + 'T' + f(dt.hour) + f(dt.minute) + '00'
            else:
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
            date = term_start + datetime.timedelta(days=((j - 1) * 7 + int(c.get('day')) - 1))
            tstart, tend = format_date(date, start_time, method), format_date(date, end_time, method)
            data = {
                "name": c.get('name'),
                'tstart': tstart,
                'tend': tend,
                'room': c.get('room'),
                'alarm': '20',
                'mdes': 'Teacher: ' + c.get('teacher'),
                'ades': ''
            }
            yield data


def get_json(js, term_start, method=None):
    """
    :param method: method for calculating time, 0 and None do nothing and 1 for Youyi Campus time schedule
    :param js: class info (json)
    :param term_start: first monday (20190826)
    :return:
    """
    res = []
    for data in get_data(js, term_start, method):
        res.append({
            "title": data['name'],
            'description': 'ClassRoom: {}\n'.format(data['room']) + data['mdes'],
            'start': data['tstart'],
            'end': data['tend'],
        })
    return res


def get_calendar(js, term_start, method=None):
    """
    :param method: method for calculating time, 0 and None do nothing and 1 for Youyi Campus time schedule
    :param js: class info (json)
    :param term_start: first monday (20190826)
    :return:
    """

    def uid():
        return ''.join([random.choice(string.ascii_letters) for i in range(20)])

    def format_template(name, tstart, tend, room, alarm, mdes='', ades=''):
        timeNow = time.strftime("%Y%m%dT%H%M%SZ", time.localtime())
        body_elem = body_template.format(
            created=timeNow, uid1=uid(), uid2=uid(), uid3=uid(), tend=tend, tstart=tstart, room=room, alarm=alarm,
            name=name, mdes=mdes, ades=ades
        )
        return body_elem

    head, body_template, tail = GetSettings.get_default_calendar_settings()
    body = []

    for data in get_data(js, term_start, method):
        body.append(format_template(**data))

    return head.format(''.join([random.choice(string.ascii_uppercase) for i in range(10)])) + '\n{}\n'.format(
        '\n'.join(body)) + tail

