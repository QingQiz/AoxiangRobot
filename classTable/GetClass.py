#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import json
from functions.ClassTable import GetClass


with open('settings/ClassTimeSetting.json', 'r', encoding='utf8') as f:
    res = GetClass.get(json.loads(f.read()))

    with open('settings/ClassInfo.json', 'w', encoding='utf8') as f2:
        f2.write(json.dumps(res, ensure_ascii=False, indent=4))

