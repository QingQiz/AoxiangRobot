#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import json
from functions.ClassTable import ClassTable


with open('settings/ClassInfo.json', encoding='utf8') as f:
    js = json.loads(f.read())
    res = ClassTable.get_calendar(js=js, term_start='20190826')

    with open('res.ics', 'w', encoding='utf8') as f2:
        f2.write(res)
