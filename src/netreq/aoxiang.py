#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def table2json(html, dataFixer=None):
    """covert table in html to json
    :param dataFixer:
    :param html: html include <table> </table>
    :return: for example:
        [
            {
                'table head1': 'table value1'
                'table head2': 'table value2'
                'table head3': 'table value3'
            }
        ]
    """
    import re

    if dataFixer is None:
        dataFixer = lambda x: x

    table = re.findall(r'<table.*?</table>', html, re.DOTALL)[-1]
    # do not set regex to r'<th.*>(.*?)</th>', this will match <thead>...<th>...</th>
    tableHeader = re.findall(r'<th .*?>(.*?)</th>', table, re.DOTALL)

    tableRows = re.findall(r'<tr.*?>(.*?)</tr>', table, re.DOTALL)[1:]
    if not tableRows: return None
    if len(tableRows) == 1 and tableRows[0].strip() == '': return None

    def row2data(row):
        """
        row may like:
            \t\t<td>20xx-20xx X</td>\r
            \t\t<td>UXXXXXXXX</td>\r
            \t\t<td>UXXXXXXXX.XX</td>\r
            <td>\t\t\t\t<a href="javascript:void(0)"  onclick="showInfo(xxxxxxxx)" >XXXXXXX</a>\r
            \t\t\r
            \t\t</td>\r
            <td>XXXXXXXXX</td>\t\t<td>xxx</td>\r
            <td style=""></td><td style=""></td><td style="">\t  \t\t\txx \r
            </td><td style="">\t  \t\t\txx \r\n</td><td style="">\t\t\t\txx\r\n\t\t\t\r
            </td><td>\t\t\t\t\txx\r
            \t\t\t\r\n</td>\t\t\r

        """
        return [dataFixer(data) for data in re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL)]

    # tableData: [[data, data]]
    tableData = list(map(row2data, tableRows))
    # [{key: data}]
    return [{tableHeader[i]: rowData[i] for i in range(len(tableHeader))} for rowData in tableData]


class Aoxiang:
    _termId = None
    _xIdToken = None
    _userInfo = None
    _accessToken = None

    def __init__(self, username, password, session=None):
        """
        :param username: username to uis.nwpu.edu.cn
        :param password: password to uis.nwpu.edu.cn
        :param session: session to use, None to create a new session
        """
        import requests
        from . import req

        if session is None:
            self.session = requests.Session()
        else:
            self.session = session

        # login to uis.nwpu.edu.cn
        loginUrl = 'https://uis.nwpu.edu.cn/cas/login'
        req(loginUrl, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/83.0.4103.116 Safari/537.36 "
        }, s=self.session)

        req(loginUrl, data={
            'username': username,
            'password': password,
            'currentMenu': 1,
            'execution': 'e1s1',
            '_eventId': 'submit',
        }, s=self.session)

        '''
        if login succeed, cookies will be:
            {
                'SESSION': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
                'TGC': 'TGT-aaaaa-aaaaaaaaaaaaaaaaaa-aaaaaaaaaaa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaacas-server-site-webapp-aaaaaaaaa-aaaaa'
            }
        '''
        assert self.session.cookies.get_dict().get('TGC'), 'login failed'

    @property
    def xIdToken(self):
        '''
        x-id-token for some apis of personal-center.nwpu.edu.cn
        '''
        if self._xIdToken:
            return self._xIdToken

        assert self.fullUserInfo
        return self._xIdToken

    def login_us(self):
        def is_login_us_success():
            return self.session.cookies.get_dict().get('GSESSIONID')

        if is_login_us_success():
            return

        # login to us.nwpu.edu.cn
        self.req("http://us.nwpu.edu.cn/eams/sso/login.action")

        '''
        if login successed, cookies will be:
            {
                'SESSION': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
                'TGC': 'TGT-aaaaa-aaaaaaaaaaaaaaaaaa-aaaaaaaaaaa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaacas-server-site-webapp-aaaaaaaaa-aaaaa',
                'GSESSIONID': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                'JSESSIONID': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            }
        '''
        assert is_login_us_success(), 'login to us.nwpu.edu.cn failed.'

        # switch language of us.nwpu.edu.cn to Chinese
        self.req('http://us.nwpu.edu.cn/eams/home.action', data={
            "session_locale": "zh_CN"
        })

    def req(self, url, headers=None, data=None, params=None):
        """
        make a request with current session
        """
        if params is None:
            params = {}
        if data is None:
            data = {}
        if headers is None:
            headers = {}

        import re
        from . import req as netreq

        while True:
            r = netreq(url, headers=headers, data=data, params=params, s=self.session)
            if re.search(r'请不要过快点击', r.text) is not None:
                __import__('time').sleep(0.5)
                continue
            return r

    @property
    def termId(self):
        """term to termId
        :return:
            {
                '学期': [秋学期Id, 春学期Id, 夏学期Id],
                ...
            }
        """
        import re
        from multiprocessing.pool import ThreadPool as Pool

        if self._termId:
            return self._termId

        self.login_us()

        res = self.req('http://us.nwpu.edu.cn/eams/dataQuery.action', data={
            'dataType': 'semesterCalendar',
            'value': 98,
            'empty': False
        }).text

        # dicts: ['{id:xx,schoolYear:"20xx-20xx",name:"X"}']
        dicts = re.findall(r'{(.*?)}', res)

        def searchAll(s, regexes):
            res = []
            for regex in regexes:
                res += re.findall(regex, s)
            return res

        # info: [[id, schoolYear, name]]
        info = Pool(16).map(lambda x: searchAll(x, [r'id:(.*?),', r'"(.*?)"']), dicts)

        res = {}
        for i in info:
            term = i[1].split('-')[0][-2:]
            if res.get(term):
                res[term].append(i[0])
            else:
                res[term] = [i[0]]
        self._termId = res

        return res

    @property
    def fullUserInfo(self):
        """get full user information
        :return: please try it
        """
        import json
        import base64

        if self._userInfo:
            return self._userInfo

        # 获取 xIdToken, 参考翱翔门户 `webpack:///./src/utils/decodeTicket.js`
        ticket: str
        ticket = self.req('https://uis.nwpu.edu.cn/cas/login?service=https://ecampus.nwpu.edu.cn/').url.split('=')[-1]
        ticket = ticket.replace("%2B", '+').replace("%3D", '=').split('.')[1]
        self._xIdToken = json.loads(base64.b64decode(ticket.encode('utf8')).decode('utf8'))['idToken']

        # 学生信息，这块在翱翔门户里
        # 之前的接口被弃用了，现在的接口获取到的信息少了很多
        res = self.req(f'https://personal-security-center.nwpu.edu.cn/api/v1/personal/user/info', headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'x-id-token': self.xIdToken
        }).json()
        assert res['code'] == 0, 'error on request, message: ' + res['message']

        # 学籍信息，这块在教务系统里
        # TODO FIXME 研究生没有教务系统，等我上研究生再说，先注释了
        # tables = self.req('http://us.nwpu.edu.cn/eams/stdDetail.action').text

        # action = re.findall(r"bg.Go\('(.*?)'", tables)
        # if action != []:
        #     tables = self.req('http://us.nwpu.edu.cn' + action[0]).text

        # tables = re.findall(r'<table.*?>(.*?)</table>', tables, re.DOTALL)

        # studentStatus = re.findall(r'<td.*?class="title".*?>(.*?)</td>.*?<td.*?>(.*?)</td>', tables[0], re.DOTALL)
        # contact = re.findall(r'<td class.*?>(.*?)</td>[\n\t\r\s]*?<td.*?>(.*?)</td', tables[-2], re.DOTALL)

        # procData = lambda data: dict(map(lambda x: (x[0].replace('：', ''), x[1]), data))

        # studentStatus = procData(studentStatus)
        # del studentStatus['']
        # contact = procData(contact)

        # res['studentStatus'] = studentStatus
        # res['contact'] = contact

        self._userInfo = res
        return self._userInfo

    @property
    def userInfo(self):
        """get user information
        :return: please try it
        """
        res = self.fullUserInfo

        return {
            "basicInformation": {
                'id': res['data']['accounts'][-1]['accountName'],
                'name': res['data']['user']['name'],
                'gender': res['data']['user']['gender'],
                'mobile': res['data']['user']['phoneNumber'],
                'email': res['data']['user']['email'],
                res['data']['user']['certificateType']: res['data']['user']['certificateNumber'],
                # org 取 accounts 信息中的最后一个，accounts 中可能包含本科和研究生的账号
                'org': res['data']['accounts'][-1]['organizationName'],
                'type': res['data']['accounts'][-1]['identityTypeName']
            },
        }

    def grade(self, *terms):
        """
        :param list(int) terms: which term grade to get, set [] to get all terms' grade, for example: grade(17, 18)
        :return: for example:
            [
                [
                    {
                        '学年学期': '20xx-20xx X',
                        '课程代码': 'Uxxxxxxxx',
                        '课程序号': 'Uxxxxxxxx.xx',
                        '课程名称': 'XXXXXXX',
                        '课程类别': 'XXXXXX',
                        '学分': 'xx',
                        '平时成绩': 'xx',
                        '期中成绩': 'xx',
                        '实验成绩': 'xx',
                        '期末成绩': 'xx',
                        '总评成绩': 'xx',
                        '最终': 'xx',
                        '绩点': 'xx'
                    }
                ]
            ]
        """
        import re
        import functools
        from multiprocessing.pool import ThreadPool as Pool

        def dataFixer(data: str):
            if data.find('href') != -1:
                return re.search(r'>(.*?)</a>', data, re.DOTALL).group(1)
            return data.strip()

        self.login_us()

        if terms:
            termId = self.termId

            gradeUrl = "http://us.nwpu.edu.cn/eams/teach/grade/course/person!search.action?semesterId="

            # foldl (\zero x -> zero + termId[x]) term []
            idSpace = functools.reduce(lambda x, y: x + termId[str(y)], terms, [])

            # us.nwpu.edu.cn won't return data if request too fast
            # therefore we cannot request data in parallel
            htmls = [self.req(gradeUrl + str(i)).text for i in idSpace]

            # parse html to json in parallel
            res = Pool(16).map(lambda x: table2json(x, dataFixer=dataFixer), htmls)
        else:
            allGradeUrl = "http://us.nwpu.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action"

            html = self.req(allGradeUrl).text
            res = [table2json(html, dataFixer=dataFixer)]

        return [i for i in res if i]

    def examInformation(self, *terms):
        """
        :param list(int) terms: terms, for example: examInformations(17, 18)
        :return: for example
            {
                '20xx-20xx学年x学期xxxx': [
                    {
                        '课程序号': 'UXXXXXXXX.XX',
                        '课程名称': 'XXXXX',
                        '考试类型': 'XXXX',
                        '考试日期': '20xx-xx-xx',
                        '考试时间': 'xx:xx~xx:xx',
                        '考场校区': 'xx校区',
                        '考场教学楼': 'XXXXXX',
                        '考场教室': 'xxxxxx',
                        '考试情况': '正常',
                        '其它说明': ''
                    }
                ]
            }
        """
        import re
        import functools

        self.login_us()

        examTableUrl = 'http://us.nwpu.edu.cn/eams/stdExamTable!examTable.action?examBatch.id='

        # same as: concatMap (\x -> termId[x]) terms
        termIds = functools.reduce(lambda zero, x: zero + self.termId[str(x)], terms, [])

        tableIds = []
        for termId in termIds:
            r = self.req('http://us.nwpu.edu.cn/eams/stdExamTable.action', data={
                'semester.id': termId
            })
            tableIds += re.findall(r'option value="(.*?)".*?>(.*?)</option>', r.text)
        # tableIds will be: {'501': '2019-2020学年秋学期期中考试', '482': '2019-2020秋课程考试', '481': '2019-2020秋补考', ...}
        tableIds = dict(tableIds)

        def dataFixer(data: str):
            if data.find('未安排的') != -1:
                return None
            if data.find('href') != -1:
                return re.search(r'>(.*?)</a>', data, re.DOTALL).group(1)
            return data.strip()

        res = {}
        for tableId in tableIds:
            html = self.req(examTableUrl + tableId).text
            json = table2json(html, dataFixer=dataFixer)

            if json:
                res[tableIds[tableId]] = json
        return res

    def myCourses(self, term):
        """get my course information
        :param int term: term
        :return: for example:
            [
                {
                    '学分': 'x',
                    '序号': 'x',
                    '操作': '',
                    '教学大纲': 'xxxxxxx',
                    '教师': 'xxxxxx',
                    '校区': 'xxxx',
                    '考试类型': 'xxxx',
                    '课程介绍': '课程链接：https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                    '课程代码': 'Uxxxxxxxx',
                    '课程名称': 'xxxx',
                    '课程安排': '',
                    '课程序号': 'Uxxxxxxxx.xx',
                    '起止周': 'x-x'
                }
            ]
        """
        import re

        def dataFixer(data: str):
            data = data.replace('<br>', '\n').strip()

            if data.find('href') != -1:
                return re.search(r'>(.*?)</a>', data, re.DOTALL).group(1)
            return data

        self.login_us()

        ids = self.req('http://us.nwpu.edu.cn/eams/courseTableForStd.action').text
        ids = re.search(r'"ids","([0-9]+)"', ids).group(1)

        res = []
        for t in self.termId[str(term)]:
            json = table2json(self.req('http://us.nwpu.edu.cn/eams/courseTableForStd!courseTable.action', data={
                'ignoreHead': 1,
                'setting.kind': 'std',
                'startWeek': 1,
                'semester.id': t,
                'ids': ids
            }).text, dataFixer=dataFixer)
            res += json if json else []
        return res

    def classTable(self, timeStart=None, timeEnd=None):
        """get classtable in json format
        :param timeStart: class time begin date, for example: 2020-08-01, default: today
        :param timeEnd: class time end date, for example: 2020-10-01, default: today + 180 days
        :return:
            [
                {
                    'startTime': 'XX:XX:XX',
                    'startDate': 'XXXX-XX-XX XX:XX:XX',
                    'startDateStr': '20XX-XX-XX',
                    'endTime': 'XX:XX:XX',
                    'endDate': '20XX-XX-XX XX:XX:XX',
                    'endDateStr': 'XXXX-XX-XX',
                    'timezone': 'XXX+XX:XX - XXXXXX',
                    'address': '[XXXX]XXYYYY'
                    'title': 'XXXXXXXXXXXX',
                    'id': 'XXXXXXXXXXXXXXXXXXXXXXXXX',
                    'color': '',
                    'calendarName': 'XX',
                    'isWholeDay': '0',
                }
            ]
        """
        import datetime, functools, random
        from multiprocessing.pool import ThreadPool as Pool

        timeFormat = '%Y-%m-%d'

        if timeStart is None:
            timeStart = datetime.date.today().strftime(timeFormat)
        if timeEnd is None:
            timeEnd = (datetime.date.today() + datetime.timedelta(days=180)).strftime(timeFormat)

        start = datetime.datetime.strptime(timeStart, timeFormat)
        end = datetime.datetime.strptime(timeEnd, timeFormat)

        params = []
        while start < end:
            nextStart = start + datetime.timedelta(days=6)

            l = start.strftime(timeFormat)
            r = (nextStart if nextStart <= end else end).strftime(timeFormat)
            params.append([l, r])

            start = nextStart + datetime.timedelta(days=1)

        def reqTable(args):
            res = self.req('https://portal-service.nwpu.edu.cn/v1/calendar/share/schedule/getEvents', params={
                'startDate': args[0],
                'endDate': args[1],
                'reqType': 'WeekView',
                'random_number': random.randint(100, 500)
            }, headers={
                'x-id-token': self.xIdToken
            }).json()

            assert res['code'] == 0, 'wrong response status, error message: ' + res['message']

            if res['data'] is None:
                return []

            return [j for i in res['data']['schedule'].values() for j in i['calendarList']]

        # request data in parallel
        ret = Pool(16).map(reqTable, params)

        return sorted(functools.reduce(lambda zero, x: zero + x, ret, []), key=lambda x: x['startDate'])

    def yqtb(self, province=None, city=None, location='在学校'):
        """疫情填报，叫 yqtb 的原因是他的那个 sb 域名是 yqtb

        :param province: 省或直辖市，在学校/在西安可为None
        :param city: 市，直辖市填市辖区或县，在学校/在西安可为None。
        :param location: 所在地: 在西安、在学校或你所在的县级行政区如: 龙游县、鸠江区、镇沅彝族哈尼族拉祜族自治县
        :return:
            {
                'state': '您已提交今日填报重新提交将覆盖上一次的信息。',
                '当前所在位置': '在学校',
                '今天的体温范围': '37.3度以下',
                '您有无疑似症状?（可多选）': '无',
                '西安市一码通状态': '绿码'
            }
        """
        import re
        import json

        uid = self.userInfo['basicInformation']['id']
        name = self.userInfo['basicInformation']['name']
        # org = self.userInfo['basicInformation']['org']

        locationDict = {
            "在学校": "1",
            "在西安": "2"
        }
        locCode = locationDict.get(location)
        if locCode is None:
            locationDict = self.req('http://yqtb.nwpu.edu.cn/wx/js/eams.area.data.js')
            locationDict = re.findall(r'{(.*)}', locationDict.text, re.DOTALL)[0]
            locationDict = json.loads('{' + locationDict + '}')

            # query location code
            for code, loc in locationDict.items():
                if code[2:] == '0000' and loc == province:
                    provCode = code[:2]
                    break
            else:
                raise KeyError(f'No such province: {province}')

            for code, loc in locationDict.items():
                if code[:2] == provCode and code[4:] == '00' and loc == city:
                    cityCode = code[:4]
                    break
            else:
                raise KeyError(f'No such city: {province}{city}')

            for code, loc in locationDict.items():
                if code[:4] == cityCode and loc == location:
                    locCode = code
                    break
            else:
                raise KeyError(f'No such place: {province}{city}{location}')

            location = province + city + location

        self.req('http://yqtb.nwpu.edu.cn/')

        # fetch mobile number
        # r = self.req('http://yqtb.nwpu.edu.cn/wx/ry/jbxx_v.jsp')
        # mobile = re.findall(r'手机号码.*?([0-9]+)', r.text, re.DOTALL)[0]

        data = {
            "hsjc": "1",  # 核酸检测，我默认你检测了，不负责
            "xasymt": "1",  # 西安市一码通
            "actionType": "addRbxx",
            "userLoginId": uid,
            # "fxzt": "9",  # 返校状态
            "userType": "2",  # 猜不出来
            "userName": name,
            "szcsbm": locCode,  # 所在城市编码
            "szcsmc": location,  # 所在城市名称（为啥是在学校啊）
            "sfyzz": "0",  # 是否有症状
            "sfqz": "0",  # 是否确诊
            "tbly": "sso",  # 填报(？留言)
            "qtqksm": "",  # 其它情况说明
            "ycqksm": "",  # ？？情况说明
            # "qrlxzt": "",  # 确认离（？留）校状态
            # "xymc": org,  # 学院名称
            # "xssjhm": mobile,  # 学生手机号码
        }

        # 学校加了点校验参数，所以不能直接请求了
        # 但是他这个校验参数直接写在了html页面里就。。。
        html = self.req('http://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp').text
        report_url = re.findall(r"url:'(ry_ut.*?)'", html)[0]

        self.req(f'http://yqtb.nwpu.edu.cn/wx/ry/{report_url}', data=data, headers={
            "Referer": "http://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp",
            "Origin": "http://yqtb.nwpu.edu.cn",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        })

        r = self.req('http://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp')

        x = re.findall(r'(?<!>)\n.*div.*weui-cells__title">(.*)</div>', r.text)
        x = list(filter(lambda x: '时间' not in x and '说明' not in x, x))
        y = re.findall(r'.*div.*\n.*<p>(.*?)<.*\n.*\n.*\n.*input.*checked.*', r.text)
        x = list(zip(x, y))

        res = {'state': re.findall(r'i class=.co4.>(.*?)</i', r.text)[0]}

        for i, j in x:
            res[i] = j

        return res
