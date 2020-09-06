#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Exam():
    def __init__(self, username=None, password=None):
        from QingQiz.netreq.aoxiang import Aoxiang

        self.aoxiang = Aoxiang(username, password)

    def output(self, *terms):
        '''
        :param terms: terms to exam information
        '''
        from datetime import datetime
        from rich.console import Console
        from rich.table import Table

        exams = self.aoxiang.examInformations(*terms)

        console = Console()

        for term in exams:
            # exam: [([head], [value]), (...)]
            exam = list(map(lambda x: list(zip(*x.items())), exams[term]))
            # exam[0][0]:
            #   课程序号 ┃ 课程名称 ┃ 考试类型 ┃ 考试日期 ┃ 考试时间 ┃ 考场校区 ┃ 考场教学… ┃ 考场教室 ┃ 考试情况 ┃ 其它说明
            # remove 课程序号 and 其它说明
            header = exam[0][0][1:-1]
            exam = list(sorted(map(lambda x: x[1][1:-1], exam), reverse=True))

            table = Table(title=term, width=120)
            rowStyles = []
            for h in header:
                table.add_column(h)
            for e in exam:
                table.add_row(*e)

                examDate = e[2] + ' ' + e[3].split('~')[-1] + ':00'
                examDate = datetime.strptime(examDate, '%Y-%m-%d %H:%M:%S')

                if datetime.now() > examDate:
                    rowStyles.append('dim')
                else:
                    rowStyles.append('none')

            table.row_styles = rowStyles

            console.print(table)
