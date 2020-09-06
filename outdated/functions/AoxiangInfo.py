#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
from . import getUserName_Password

urlLogin = 'http://us.nwpu.edu.cn/eams/login.action'


def login(username, password, headers):
    url = 'https://uis.nwpu.edu.cn/cas/login'

    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    })

    s.get(url)
    s.post(url, data={
        'username': username,
        'password': password,
        'currentMenu': 1,
        'execution': 'e1s1',
        '_eventId': 'submit',
    })
    return s


def get(url, headers={}, cookies={}, username=None, password=None):
    conn = check(username, password, headers)
    return conn.get(url, headers=headers, cookies=cookies).text


def post(url, headers={}, cookies={}, data={}, username=None, password=None):
    conn = check(username, password, headers)
    return conn.post(url, headers=headers, cookies=cookies, data=data).text


def check(username, password, header={}):
    conn = login(username, password, header)
    url = conn.get('http://us.nwpu.edu.cn/eams/home!index.action').url
    if url.find('login') >= 0:
        raise ValueError('Invalid username or password')
    return conn

