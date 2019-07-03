#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
sys.path.append('..')
from functions import getUserName_Password


def login(headers={}):
    userName, password = getUserName_Password.get(is_input=False)

    dataLogin = {
        'username': userName,
        'password': password,
        'session_locale': 'zh_CN',
    }
    urlLogin = 'http://us.nwpu.edu.cn/eams/login.action'

    conn = requests.session()
    conn.post(url=urlLogin, data=dataLogin, headers=headers)
    return conn


def get(url, headers={}, cookies={}):
    conn = login()
    return conn.get(url, headers=headers, cookies=cookies).text


def post(url, headers={}, cookies={}, data={}):
    conn = login()
    return conn.post(url, headers=headers, cookies=cookies, data=data).text
