#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
from . import getUserName_Password

urlLogin = 'http://us.nwpu.edu.cn/eams/login.action'


def login(username, password, headers):
    if username is None or password is None:
        username, password = getUserName_Password.get(is_input=False)

    dataLogin = {
        'username': username,
        'password': password,
        'session_locale': 'zh_CN',
    }

    conn = requests.session()
    conn.post(url=urlLogin, data=dataLogin, headers=headers)
    return conn


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

