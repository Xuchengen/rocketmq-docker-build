import re
import traceback

import requests


class Item:
    def __init__(self):
        self.version = None
        self.datetime = None


# 获取版本清单
def get_version_list() -> list[Item]:
    try:
        url = "https://archive.apache.org/dist/rocketmq/"
        resp = requests.get(url)
        html = resp.text

        result = re.findall("<a href=\".*?/\">(\\d+.*?)/</a>\\s+(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2})", html)

        if len(result) == 0:
            raise Exception("正则提取失败，提取结果：%s条" % len(result))

        result_list = []
        for e in result:
            item = Item()
            item.version = e[0]
            item.datetime = e[1]
            result_list.append(item)

        return result_list

    except Exception as e:
        print("错误：解析Apache Rocketmq archive异常！%s" % e)
        traceback.print_exc()
        exit()
