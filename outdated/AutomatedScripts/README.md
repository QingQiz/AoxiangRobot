### 这里是一些自动化脚本

- `evaluation.py`
  自动评教

- `EnglishL.py`
  自动做英语听力, 脚本已完成, 但是还没有录入答案 ~懒得录啊......~

### 依赖库

- python
  - selenium

- chrome
  - chromedriver

### 配置文件格式

- `answer/bookid.json`

  - 对于听说教程

    ```json
    {
        "unit": {
            "LSC": {
                "type": type,
                "answer": string/list
            },
            "LLC": {
                "type": type,
                "answer": string/list
            },
            "LPS": {
                "type": type,
                "answer": string/list
            },
            "LRP": {
                "type": type,
                "answer": string/list
            },
            "HLC": {
                "type": type,
                "answer": string/list
            },
            "HPS": {
                "type": type,
                "answer": string/list
            },
            "HCD": {
                "type": type,
                "answer": string/list
            }
        }
    }
    ```

    - 其中LSC, LLC, LPS, LRP, HLC, HPS, HCD分别是Listening中的Short Conversation, Long Conversation, Passage, Radio Program和Homework中的Long Conversation, Passage, Compound Dictation的缩写

    - type 和 题目类型的对应关系:

    | type | 题目类型 |
    | ---- | -------- |
    | 0    | 多选     |
    | 1    | 短对话   |
    | 2    | 填空     |


  - 对于视听说教程

    ```json
    {
        "unit": {
            "OV": {
                "problem number": {
                    "type": type,
                    "answer": string/list
                },
            },
            "LS": {
                "problem number": {
                    "type": type,
                    "answer": string/list
                }
            },
            "UT": {
                "type": type,
                "answer": string/list
            }
        }
    }
    ```

    - 类似听说教程的格式, 只不过OV代表Outside view, LS代表Listening, UT代表Unit test,
    - Problem Number代表答题中间的小题号, 比如Listening下有一个Talk和两个Passage, 就依次排为1,2,3,4,5

    - type 和 题目类型的对应关系:

    | type | 题目类型                          |
    | ---- | --------------------------------- |
    | 0    | 选择你同意的陈述                  |
    | 1    | 多选                              |
    | 2    | 填空                              |
    | 3    | 拖动排序                          |
    | 4    | 在一个表格中填空                  |
    | 5    | 在一个文本框里输入                |
    | 6    | 从下拉菜单中选择                  |

    **NOTE**:

    - 对于在一个表格中选择的题, 从0开始, 从左到右从上到下计数, 哪个需要选择, 答案就是当前计数
    - 对于拖动排序, 在json中只写正确的顺序
    - 文本框这类题一般不要求做
    - 表格中填空和下拉菜单的题不多见

