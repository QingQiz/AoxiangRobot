#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ClassTable():
    def __init__(self, username, password):
        from QingQiz.netreq.aoxiang import Aoxiang

        self.aoxiang = Aoxiang(username, password)

    def output(self, timeStart, timeEnd, **kwargs):
        '''
        :param timeStart:
        :param timeEnd:
        :param **kwargs:
            output: output file
            alarm: alarm before event
        '''
        classTable = self.aoxiang.classTable(timeStart, timeEnd)

        if kwargs['output']:
            raise NotImplementedError('TODO')
        else:
            from rich.console import Console
            from rich.table import Table

            console = Console()

            table = Table(title=f'{timeStart} - {timeEnd} 课表', width=120)

            header = ['title', 'start', 'end', 'location']

            for h in header:
                table.add_column(h)

            for ev in classTable:
                table.add_row(*[ev[h] for h in header])

            table.row_styles = ['none', 'dim']

            console.print(table)
