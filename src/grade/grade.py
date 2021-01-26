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
        from rich.markdown import Markdown

        grades = self.aoxiang.grade(*terms)
        grade_sum = 0
        score_sum = 0

        gpa_exclude = []

        console = Console()

        def is_number(num):
            import re
            pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
            return bool(pattern.match(num))

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
                table.add_column(h.replace('成绩', ''))
            for g in grade:
                g = list(g)

                # 修复sb教务乱显示的成绩
                g[-2] = g[-2][:2] if g[-2] != '100' else g[-2]
                g[-2] = '95' if g[-2] == 'A' else g[-2]
                table.add_row(*g)

                if (is_number(g[-2][:2])) and is_number(g[-1]):
                    grade_sum += float(g[2])
                    score_sum += float(g[-2])*float(g[2])
                else:
                    gpa_exclude.append((g[0], g[-2][:2], g[-1]))

            table.row_styles = ['none', 'dim']

            console.print(table)

            md =  "GPA **排除**:\n" + "\n\n".join(map(lambda x: f'- **{x[0]}**: *{x[1]}*, *{x[2]}*', gpa_exclude))
            md += f"\n\n共 **{len(grade)}** 门课程，学分绩估算： **{score_sum / grade_sum :.2f}**"

            console.print(Markdown(md))
            console.print("\n")
