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


def remove_chars(s, *args):
    if s is None:
        return s
    for char in args:
        s = s.replace(char, '')
    return s


def replace_chars(s, **kwargs):
    if s is None:
        return s
    for key, value in kwargs.items():
        s = s.replace(key, value)
    return s
