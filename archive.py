from html.parser import HTMLParser

import requests


def get_version_list():
    url = "https://archive.apache.org/dist/rocketmq/"
    resp = requests.get(url)
    parser = __ApacheRocketmqArchiveHTMLParser()
    parser.feed(resp.text)
    return parser.result_list


class Item:
    def __init__(self):
        self.version = None
        self.date_time = None


class __ApacheRocketmqArchiveHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.__img_flag = False
        self.__a_flag = False
        self.__a_end_flag = False
        self.result_list = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.__img_flag is False and tag == "img" and ("alt", "[DIR]") in attrs:
            self.__img_flag = True

        # 判断上一个标签为img且alt为[DIR]并且当前标签为a才有意义
        if self.__img_flag and tag == "a":
            self.__a_flag = True

    def handle_data(self, data: str) -> None:
        # 当前为a标签提取版本号
        if self.__a_flag:
            self.__img_flag = False
            self.__a_flag = False

            if not (len(data) > 0
                    and (data.find("dashboard") > 0
                         or data[0:1].isnumeric())):
                return

            self.__a_end_flag = True

            item = Item()
            item.version = data.removesuffix("/")
            self.result_list.append(item)
            return

        # a标签结束提取发布日期
        if self.__a_end_flag:
            self.__a_end_flag = False
            item = self.result_list[-1]
            item.date_time = data.replace("    -   ", "").strip(" ")
