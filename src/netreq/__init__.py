#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


def req(url, headers=None, data=None, params=None, encoding='', s=None):
    if params is None:
        params = {}
    if data is None:
        data = {}
    if headers is None:
        headers = {}
    if s is None:
        s = requests.Session()

    s.headers.update(headers)

    if data:
        r = s.post(url, data=data)
    else:
        r = s.get(url, params=params)

    if encoding:
        r.encoding = encoding

    return r


def url_content(url, encoding='', headers=None, data=None, params=None, s=None):
    if params is None:
        params = {}
    if data is None:
        data = {}
    if headers is None:
        headers = {}
    r = req(url, headers, data, params, s)

    if r.encoding:
        r.encoding = encoding

    return r.content


def url_html(url, encoding='', headers=None, data=None, params=None, s=None):
    if params is None:
        params = {}
    if data is None:
        data = {}
    if headers is None:
        headers = {}
    r = req(url, headers, data, params, s)

    if r.encoding:
        r.encoding = encoding

    return r.text


def url_json(url, encoding='', headers=None, data=None, params=None, s=None):
    if params is None:
        params = {}
    if data is None:
        data = {}
    if headers is None:
        headers = {}
    r = req(url, headers, data, params, s)

    if r.encoding:
        r.encoding = encoding

    return r.json()
