## 这是翱翔门户的一个爬虫


### Install Requirements

`pip install --upgrade -r requirements.txt`

### Examples

**注意**: 应将密码写入一个文件中，并向 `-p/--password` 参数传入文件路径

- 获取 2019、2020 学年的成绩

  `./aoxiangRobot -u 2017000000 -p ./password grade -t 19 20`

- 获取 2019 学年的考试安排

  `./aoxiangRobot -u 2017000000 -p ./password exam -t 19`

- 获取 *今天* 到 *今天 + 180 天* 期间的课表，输出 res.ics，格式为 [iCalendar (ICS)](https://zh.wikipedia.org/wiki/ICalendar)，每节课之前 `20 min` 提醒

  `./aoxiangRobot -u 2017000000 -p ./password classTable -o res.ics -a 20`

- 疫情填报

  `./aoxiangRobot -u 2017000000 -p ./password yqtb`

  `./aoxiangRobot -u 2017000000 -p ./password yqtb -l 西安`

- 详见: `./aoxiangRobot --help` 或 `./aoxiangRobot sub-command -h`
