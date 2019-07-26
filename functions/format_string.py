#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def width(string):
    if string is None:
        return 0
    jud = lambda x: u'\u4e00' <= x <= u'\u9fa6'
    length = 0
    for char in string: length += 2 if jud(char) else 1
    return length


def format(string, num, color=''):
    string = string.replace('（', '(').replace('）', ')')
    string = string.strip()

    blk_n = num - width(string)

    string += '\033[m' + ' ' * blk_n
    string = string.replace('实验', '\033[32m实验\033[m')
    return color + string
