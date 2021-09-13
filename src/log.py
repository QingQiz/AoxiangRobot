#!/usr/bin/env python3

import rich
import datetime


INFO = '[bold blue]II[/bold blue]'
WARN = '[bold yellow]WW[/bold yellow]'
ERR  = '[bold red]EE[/bold red]'


def print_head(level):
    if level not in [INFO, WARN, ERR]:
        raise TypeError()

    print('[', end='')
    rich.print(level, end='', flush=True)
    print(']', end=' ')


def w(msg):
    print_head(WARN)
    print(msg, flush=True)


def e(msg):
    print_head(ERR)
    print(msg)
    exit(-1)


def i(msg):
    print_head(INFO)
    print(msg)


def d(msg, end='\n', **kwargs):
    if 'DEBUG' not in kwargs:
        return
    if not kwargs['DEBUG']:
        return
    print('[DEBUG]', msg, end=end)


def t(msg, level=INFO):
    print('[', end='')
    rich.print(f'[bold green]{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}[/bold green]', end='')
    print(']', end=' ')
    print_head(level)
    print(msg, flush=True)


def yes_or_no(msg):
    ans = str(input(f'{msg} (y/N) ')).lower().strip()
    return ans == 'y'
