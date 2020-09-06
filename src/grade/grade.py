#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Grade():
    def __init__(self, username=None, password=None):
        from QingQiz.netreq.aoxiang import Aoxiang

        self.aoxiang = Aoxiang(username, password)

    def output(self, *terms):
        '''
        :param terms: terms to get grade
        '''
        from rich.console import Console
        from rich.table import Table

        grades = self.aoxiang.grade(*terms)

        console = Console()

        # grade: [{head: value, head: value}, {...}]
        for grade in grades:
            # grade: [([head], [value]), (...)]
            grade = list(map(lambda x: list(zip(*x.items())), grade))
            # header:
            #   学年学期 ┃ 课程代码 ┃ 课程序号 ┃ 课程名称 ┃ 课程类别 ┃ 学分 ┃ 平时成绩 ┃ 期中成绩 ┃ 实验成绩 ┃ 期末成绩 ┃ 总评成绩 ┃ 最终 ┃ 绩点
            header = grade[0][0]
            title = grade[0][1][0] if terms else 'All Terms'
            grade = list(sorted(map(lambda x: x[1][3:], grade), reverse=True))

            table = Table(title=title, width=120)
            for h in header[3:]:
                table.add_column(h)
            for g in grade:
                table.add_row(*g)
            table.row_styles = ['dim', 'none']

            console.print(table)
