#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import json
from functions.ClassTable import ClassTable

try:
    method = input('ChangAn Campus[*0] or Youyi Campus[1] or custom settings[2]? _\b')
    if method not in ('', '0', '1', '2'):
        print('input [0/1/2] please.')
        exit(-1)
    method = int(method if method != '' else '0')
    method = None if method == 2 else method

    with open('settings/ClassInfo.json', encoding='utf8') as f:
        js = json.loads(f.read())
        res = ClassTable.get_calendar(js=js, term_start='20190826', method=method)

        with open('res.ics', 'w', encoding='utf8') as f2:
            f2.write(res)

except KeyboardInterrupt:
    print('\nInterrupted')
    exit(0)



