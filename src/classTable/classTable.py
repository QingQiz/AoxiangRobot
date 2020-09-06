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
            :output str: output file
            :alarm int: alarm before event
        '''
        if kwargs['output']:
            import os
            from .ics import ICS
            from QingQiz import log

            if os.path.exists(kwargs['output']):
                log.e('file exists')

            classTable = self.aoxiang.classTable(timeStart, timeEnd)

            header = ICS.header(f'{timeStart} - {timeEnd} 课表')

            body = []
            for ct in classTable:
                body.append(ICS.body(name=ct['title']
                    , start=ct['start']
                    , end=ct['end']
                    , location=ct['location']
                    , description=''
                    , alarm=kwargs['alarm']
                     , alarmDescription=''))
            body = '\n'.join(body)

            footer = ICS.footer()

            with open(kwargs['output'], 'w') as f:
                print(header, file=f)
                print(body, file=f)
                print(footer, file=f)
        else:
            from rich.console import Console
            from rich.table import Table

            classTable = self.aoxiang.classTable(timeStart, timeEnd)

            console = Console()

            table = Table(title=f'{timeStart} - {timeEnd} 课表', width=120)

            header = ['title', 'start', 'end', 'location']

            for h in header:
                table.add_column(h)

            for ev in classTable:
                table.add_row(*[ev[h] for h in header])

            table.row_styles = ['none', 'dim']

            console.print(table)
