#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ICS():
    @staticmethod
    def header(name):
        return f"""BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:ClassTable[{name}]
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
END:VTIMEZONE"""

    @staticmethod
    def footer():
        return """END:VCALENDAR"""

    @staticmethod
    def body(name, start, end, location, description, alarm, alarmDescription):
        import random, string, time

        def uid():
            return ''.join([random.choice(string.ascii_letters) for i in range(20)])

        timeNow = time.strftime("%Y%m%dT%H%M%SZ", time.localtime())

        return f"""BEGIN:VEVENT
CREATED:{timeNow}
UID:{uid()}@github.com/QingQiz
DTEND;TZID=Asia/Shanghai:{end}
TRANSP:OPAQUE
X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC
SUMMARY:{name}
DTSTART;TZID=Asia/Shanghai:{start}
DTSTAMP:{timeNow}Z
LOCATION:{location}
DESCRIPTION:{description}
SEQUENCE:0
BEGIN:VALARM
X-WR-ALARMUID:{uid()}@github.com/QingQiz
UID:{uid()}@github.com/QingQiz
TRIGGER:-PT{alarm}M
DESCRIPTION:{alarmDescription}
ACTION:DISPLAY
END:VALARM
END:VEVENT"""
