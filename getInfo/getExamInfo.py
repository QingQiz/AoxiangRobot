#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从翱翔门户获取考试安排和考试成绩
TODO 学分绩
TODO 期中考试的安排...
FIXME 表格的ID似乎很奇怪，只能先每学期都改改了
"""
import datetime
import sys

sys.path.append('..')
from functions import Grade, Exam
from functions import format_string as fs


long_len, short_len = 0, 8

DEBUG = 0


def table_info():
    global exam, grade, grade_index, long_len, short_len
    grade, exam = Grade.get(Id=36), Exam.get(Id=382)
    try:
        dic = {key: 0 for key in grade[0]}
        for i in grade:
            for key in i:
                dic[key] += 1 if i[key] is not None else 0
                if key != 'name':
                    short_len = max(short_len, fs.width(i[key]))
            long_len = max(long_len, fs.width(i['name']))
        grade_index = [key for key in dic if dic[key] != 0]
    except IndexError:
        pass
    try:
        for key in exam[0]:
            exam_index.append(key)
        exam_ = []
        for i in exam:
            if not DEBUG:
                et = i['date'].split('-')
                et.extend(i['time'].split('~')[-1].split(':'))

                et = datetime.datetime(*map(int, et))
                if datetime.datetime.now() < et:
                    exam_.append(i)
        exam = exam_ if not DEBUG else exam

        for i in exam:
            for key in i:
                if key != 'name':
                    short_len = max(short_len, fs.width(i[key]))
            long_len = max(long_len, fs.width(i['name']))
    except IndexError:
        pass
    long_len += 2
    short_len += 2
    len_grade = long_len + (len(grade_index) - 1) * short_len
    len_exam = long_len + (len(exam_index) - 1) * short_len
    return max(len_exam, len_grade)


def format_json(json, index, header={}):
    lines = []
    for dic in json:
        def dyeing(idx):
            if dic[idx] is None:
                return fs.format('-', short_len)
            if idx == 'name':
                return fs.format(dic[idx], long_len)

            if idx in ['final', 'total', 'makeUp']:
                value = dic[idx]
                try:
                    value = float(value)
                    return fs.format(dic[idx], short_len, '' if value >= 60 and not DEBUG else '\033[31m')
                except ValueError:
                    value = value.replace('-', '')
                    value = value.replace(' ', '')
                    value = value.replace('（', '')
                    value = value.replace('）', '')
                    value = value.replace('(', '')
                    value = value.replace(')', '')
                    value = value.replace("申请", "")
                    return fs.format(value, short_len)
            return fs.format(dic[idx], short_len)

        lines.append(''.join([dyeing(key) for key in index]))

    result = '\n'.join(sorted(lines)[::-1])

    if result == '':
        return ''

    head = ''.join([fs.format(header[i], long_len if i == 'name' else short_len) for i in index])
    return head + '\n' + table_len * '-' + '\n' + result


if __name__ == '__main__':
    # 第一学期17, 第二学期35, 上学期18, 本学期为36
    grade, exam, grade_index, exam_index = [], [], [], []
    table_len = table_info()

    exam_formatted = format_json(exam, exam_index, Exam.header)
    grade_formatted = format_json(grade, grade_index, Grade.header)

    if bool(exam_formatted):
        print(table_len * '=')
        print(exam_formatted)
        print('\n' + table_len * '=')

    if bool(grade_formatted):
        if not bool(exam_formatted):
            print(table_len * '=')
        print(grade_formatted)
        print(table_len * '=')
