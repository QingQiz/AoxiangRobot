#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def get_default_time_settings(method=0):
    """
    :param method: 0 for new campus and 1 for Old campus
    :return: class time setting base
    """
    if method not in (0, 1):
        raise ValueError('method must in (0, 1)')
    ts_new = [
        {
            "name": "1",
            "during": "45",
            "time": {
                "start": "0830"
            }
        },
        {
            "name": "2",
            "during": "45",
            "offset": "10"
        },
        {
            "name": "3",
            "during": "45",
            "offset": "20"
        },
        {
            "name": "4",
            "during": "45",
            "offset": "10"
        },
        {
            "name": "5",
            "during": "45",
            "offset": "10"
        },
        {
            "name": "6",
            "during": "45",
            "offset": "0"
        },
        {
            "name": "7",
            "during": "45",
            "offset": "10"
        },
        {
            "name": "8",
            "during": "45",
            "offset": "10"
        },
        {
            "name": "9",
            "during": "45",
            "offset": "20"
        },
        {
            "name": "10",
            "during": "45",
            "offset": "10"
        },
        {
            "name": "11",
            "during": "45",
            "time": {
                "start": "1900"
            }
        },
        {
            "name": "12",
            "during": "45",
            "offset": "10"
        },
        {
            "name": "13",
            "during": "45",
            "offset": "0"
        }
    ]
    # index 0 for winter and 1 for summer
    ts_old = [
        {
            "name": "1",
            "during": "50",
            "time": {
                "start": "0800"
            }
        },
        {
            "name": "2",
            "during": "50",
            "offset": "10"
        },
        {
            "name": "3",
            "during": "50",
            "offset": "20"
        },
        {
            "name": "4",
            "during": "50",
            "offset": "10"
        },
        {
            "name": "5",
            "during": "0",
            "offset": "0"
        },
        {
            "name": "6",
            "during": "0",
            "offset": "0"
        },
        {
            "name": "7",
            "during": "50",
            "time": {
                "start": "1400"
            }
        },
        {
            "name": "8",
            "during": "50",
            "offset": "10"
        },
        {
            "name": "9",
            "during": "50",
            "offset": "20"
        },
        {
            "name": "10",
            "during": "50",
            "offset": "10"
        },
        {
            "name": "11",
            "during": "50",
            "time": {
                "start": "1900"
            }
        },
        {
            "name": "12",
            "during": "50",
            "offset": "10"
        },
        {
            "name": "13",
            "during": "0",
            "offset": "0"
        }
    ]
    if method == 1:
        return ts_old
    if method == 0:
        return ts_new


def get_default_calendar_settings():
    return """BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:ClassTable[{}]
PRODID:-//Arch Linux
X-APPLE-CALENDAR-COLOR:#FC4208
X-WR-TIMEZONE:Asia/Shanghai
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
BEGIN:STANDARD
TZOFFSETFROM:+0800
RRULE:FREQ=YEARLY;UNTIL=19910914T150000Z;BYMONTH=9;BYDAY=3SU
DTSTART:19890917T000000
TZNAME:GMT+8
TZOFFSETTO:+0800
END:STANDARD
BEGIN:DAYLIGHT
TZOFFSETFROM:+0800
DTSTART:19910414T000000
TZNAME:GMT+8
TZOFFSETTO:+0800
RDATE:19910414T000000
END:DAYLIGHT
END:VTIMEZONE""", """BEGIN:VEVENT
CREATED:{created}
UID:{uid1}@github.com/QingQiz
DTEND;TZID=Asia/Shanghai:{tend}
TRANSP:OPAQUE
X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC
SUMMARY:{name}
DTSTART;TZID=Asia/Shanghai:{tstart}
DTSTAMP:{created}Z
LOCATION:{room}
DESCRIPTION:{mdes}
SEQUENCE:0
BEGIN:VALARM
X-WR-ALARMUID:{uid2}@github.com/QingQiz
UID:{uid3}@github.com/QingQiz
TRIGGER:-PT{alarm}M
DESCRIPTION:{ades}
ACTION:DISPLAY
END:VALARM
END:VEVENT""", """END:VCALENDAR"""
