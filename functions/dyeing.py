#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform

os = platform.system().lower()

if os == 'windows':
    # Foreground
    FOREGROUND_DARKBLUE    = 0x01 # dark blue.
    FOREGROUND_DARKGREEN   = 0x02 # dark green.
    FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
    FOREGROUND_DARKRED     = 0x04 # dark red.
    FOREGROUND_DARKPINK    = 0x05 # dark pink.
    FOREGROUND_DARKYELLOW  = 0x06 # dark yellow.
    FOREGROUND_DARKWHITE   = 0x07 # dark white.
    FOREGROUND_DARKGRAY    = 0x08 # dark gray.
    FOREGROUND_BLACK       = 0x00 # black.
    FOREGROUND_RED         = 0x0c # red.
    FOREGROUND_GREEN       = 0x0a # green.
    FOREGROUND_YELLOW      = 0x0e # yellow.
    FOREGROUND_BLUE        = 0x09 # blue.
    FOREGROUND_PINK        = 0x0d # pink.
    FOREGROUND_SKYBLUE     = 0x0b # skyblue.
    FOREGROUND_WHITE       = 0x0f # white.
    # Background
    BACKGROUND_DARKBLUE    = 0x10 # dark blue.
    BACKGROUND_DARKGREEN   = 0x20 # dark green.
    BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
    BACKGROUND_DARKRED     = 0x40 # dark red.
    BACKGROUND_DARKPINK    = 0x50 # dark pink.
    BACKGROUND_DARKYELLOW  = 0x60 # dark yellow.
    BACKGROUND_DARKWHITE   = 0x70 # dark white.
    BACKGROUND_DARKGRAY    = 0x80 # dark gray.
    BACKGROUND_RED         = 0xc0 # red.
    BACKGROUND_GREEN       = 0xa0 # green.
    BACKGROUND_YELLOW      = 0xe0 # yellow.
    BACKGROUND_BLUE        = 0x90 # blue.
    BACKGROUND_PINK        = 0xd0 # pink.
    BACKGROUND_SKYBLUE     = 0xb0 # skyblue.
    BACKGROUND_WHITE       = 0xf0 # white.
    import ctypes

    def dyeing(s, foreground=FOREGROUND_BLACK, background=BACKGROUND_WHITE):
        std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle,\
                foreground | background)
        print(s, end='')
        ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle,\
                FOREGROUND_WHITE | BACKGROUND_BLACK)
else:
    # Foreground
    FOREGROUND_BLACK       = 30   # black.
    FOREGROUND_RED         = 31   # red.
    FOREGROUND_GREEN       = 32   # green.
    FOREGROUND_YELLOW      = 33   # yellow.
    FOREGROUND_BLUE        = 34   # blue.
    FOREGROUND_PINK        = 35   # pink.
    FOREGROUND_SKYBLUE     = 36   # skyblue.
    FOREGROUND_WHITE       = 37   # white.
    # Background
    BACKGROUND_BLACK       = 40   # black.
    BACKGROUND_RED         = 41   # red.
    BACKGROUND_GREEN       = 42   # green.
    BACKGROUND_YELLOW      = 43   # yellow.
    BACKGROUND_BLUE        = 44   # blue.
    BACKGROUND_PINK        = 45   # pink.
    BACKGROUND_SKYBLUE     = 46   # skyblue.
    BACKGROUND_WHITE       = 47   # white.

    def dyeing(s, foreground=FOREGROUND_BLACK, background=BACKGROUND_WHITE):
        color = '\033[1;{};{}m'.format(foreground, background)
        default = '\033[m'
        print(color + s + default, end='')


