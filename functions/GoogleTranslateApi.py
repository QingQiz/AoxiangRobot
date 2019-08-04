#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, json, execjs


def GoogleTranslateToken(text):
    GetToken = \
    """
    function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;
        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";
        for(var e=[], f=0, g=0;g < a.length; g++) {
            var m = a.charCodeAt(g);
            if (m < 128) {
                e[f++] = m;
            } else {
                if (m < 2048) {
                    e[f++] = m >> 6 | 192;
                } else {
                    if ((m & 64512) == 55296 && g + 1 < a.length && (a.charCodeAt(g + 1) & 64512) == 56320) {
                        m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023);
                        e[f++] = m >> 18 | 240;
                        e[f++] = m >> 12 & 63 | 128;
                    } else {
                        e[f++] = m >> 12 | 224;
                    }
                    e[f++] = m >> 6 & 63 | 128;
                }
                e[f++] = m & 63 | 128;
            }
        }
        a = b;
        for(f=0; f < e.length; f++) {
            a += e[f];
            a = RL(a, $b);
        }
        a = RL(a, Zb);
        a ^= b1 || 0;
        if (a < 0) {
            a = (a & 2147483647) + 2147483648;
        }
        a %= 1E6;
        return a.toString() + jd + (a ^ b);
    };

    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for(var c=0; c<b.length - 2; c += 3){
            var d = b.charAt(c + 2);
            if (d >= t) {
                d = d.charCodeAt(0) - 87;
            } else {
                d = Number(d);
            }
            if (b.charAt(c + 1) == Yb) {
                d = a >>> d;
            } else {
                d = a << d;
            }
            if (b.charAt(c) == Yb) {
                a = a + d & 4294967295;
            } else {
                a = a ^ d;
            }
        }
        return a;
    };
    """
    GetToken = execjs.compile(GetToken)
    return GetToken.call("TL", text)


def translate(*args, fromLan='en', toLan='zh-CN'):
    url = 'https://translate.google.cn/translate_a/single'
    res = []
    for text in args:
        r = requests.get(url, params=[
            ('client', 't'), ('sl', fromLan), ('tl', toLan), ('dt', 'bd'),
            ('dt', 'rm'),  ('dt', 't'), ('dt', 'qca'),
            ('tk', str(GoogleTranslateToken(text))), ('q', text),
        ])
        result = {"result": []}
        j = json.loads(r.text)
        try:
            for x in j[0]:
                if x[0] is not None:
                    result['result'].append(x[0])
        except TypeError:
            result['result'] = translate(text)[0]['result']

        try:
            for x in j[1]:
                if len(x) < 2:
                    continue
                a, b, b = x[0], x[1], str(x[1])
                result[a] = result[a] if result.get(a) is not None else []
                for k in json.loads(b.replace("'", '"')):
                    result[a].append(k)
        except (IndexError, TypeError):
            pass
        res.append(result)
    return res


if __name__ == '__main__':
    print(translate('apple'))
    print(translate('translate'))
    print(translate(''))
    print(translate('fly'))
