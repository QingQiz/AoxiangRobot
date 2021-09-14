#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


_proxy_dict = None


def req(url, headers=None, data=None, params=None, encoding='', s=None):
    if params is None:
        params = {}
    if data is None:
        data = {}
    if headers is None:
        headers = {}
    if s is None:
        s = requests.Session()

    global _proxy_dict
    if _proxy_dict is None:
        from urllib import request

        proxy_dict = request.getproxies()
        _proxy_dict = {}

        if proxy_dict:
            _proxy_dict['http'] = proxy_dict.get('http')
            if proxy_dict.get('https'):
                if '127.0.0.1' in proxy_dict['https'] or 'localhost' in proxy_dict['https']:
                    _proxy_dict['https'] = proxy_dict['https'].replace('https', 'http')
                else:
                    _proxy_dict['https'] = proxy_dict['https'].replace('https', 'http')
            _proxy_dict['ftp'] = proxy_dict.get('ftp')
            _proxy_dict = {i: j for i, j in _proxy_dict.items() if j is not None}

    s.headers.update(headers)

    if data:
        r = s.post(url, data=data, proxies=_proxy_dict)
    else:
        r = s.get(url, params=params, proxies=_proxy_dict)

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
