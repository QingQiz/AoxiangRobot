#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import json
from functions.ClassTable import GetClass


try:
    method = input('new campus[*0] or old campus[1]? _\b')
except KeyboardInterrupt:
    print('\nInterrupted')
    exit(0)

if method not in ('', '0', '1'):
    print('input [0/1] please.')
    exit(-1)

method = int(method if method != '' else '0')

res = GetClass.get(method)

with open('settings/ClassInfo.json', 'w', encoding='utf8') as f2:
    f2.write(json.dumps(res, ensure_ascii=False, indent=4))

