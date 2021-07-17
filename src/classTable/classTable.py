#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ClassTable():
    def __init__(self, username, password):
        from QingQiz.netreq.aoxiang import Aoxiang

        self.aoxiang = Aoxiang(username, password)

    def export(self, timeStart, timeEnd, **kwargs):
        '''export classTable in ics format
        :param timeStart:
        :param timeEnd:
        :param **kwargs:
            :output str: output file
            :alarm int: alarm before event
        '''
        from .ics import ICS

        classTable = self.aoxiang.classTable(timeStart, timeEnd)

        header = ICS.header(f'{timeStart} - {timeEnd} 课表')

        body = []
        for ct in classTable:
            body.append(ICS.body(name=ct['title']
                , start=ct['startDate'].replace('-', '').replace(' ', 'T').replace(':', '')
                , end=ct['endDate'].replace('-', '').replace(' ', 'T').replace(':', '')
                , location=ct['address']
                , description=ct['id']
                , alarm=kwargs['alarm']
                , alarmDescription=''))
        body = '\n'.join(body)

        footer = ICS.footer()

        with open(kwargs['output'], 'w', encoding='utf8') as f:
            print(header, file=f)
            print(body, file=f)
            print(footer, file=f)

    def output(self, term):
        '''output current courses
        :param term: term, for example: 19
        '''
        import functools
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(title=f'20{term} 我的课程')

        myCourses = self.aoxiang.myCourses(term)
        # header:
        #     0      1          2           3      4      5     6      7         8       9          10        11       12
        #   序号 ┃ 课程序号 ┃ 课程代码 ┃ 课程名称 ┃ 教师 ┃ 学分 ┃ 校区 ┃ 课程安排 ┃ 起止周 ┃ 课程介绍 ┃ 教学大纲 ┃ 考试类型 ┃ 操作
        header = list(map(lambda x: x[0], myCourses[0].items()))
        # only pick up [3, 5, ..]
        header = functools.reduce(lambda zero, x: zero + [header[x]], [3, 5, 6, 7, 8, 9, 11], [])

        for h in header:
            table.add_column(h)
        for course in myCourses:
            table.add_row(*[course[h] for h in header])

        table.row_styles = ['none', 'dim']

        console.print(table)
