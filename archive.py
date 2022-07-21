import re
import time
import traceback

import requests
from prettytable import prettytable

from constant import const
from context import Context
from helper import Helper


class VersionInfo(object):
    """
    版本信息
    """

    def __init__(self):
        """
        构造方法
        """
        self.name = None
        self.version = None
        self.datetime = None


class Archive(object):
    """
    Apache档案
    """

    regex_html = re.compile("<a href=\".*?/\">(\\d+.*?)/</a>\\s+(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2})")

    def __init__(self, page_size=10):
        """
        构造方法

        :param page_size: 页大小
        """

        self.__listener = None
        self.__rocketmq_list: list[VersionInfo] = []
        self.__console_list: list[VersionInfo] = []
        self.__page_size = page_size

    def __select(self, title: str, list_: list[VersionInfo]) -> VersionInfo:
        """
        选择

        :param title: 标题
        :param list_: 版本信息列表
        :return: 版本信息
        """

        len_ = len(list_)

        if len_ <= self.__page_size:
            return self.__all(title, list_, len_)
        else:
            return self.__page(title, list_, len_)

    def __page(self, title: str, list_: list[VersionInfo], len_: int) -> VersionInfo:
        """
        将版本信息列表数据按分页处理

        :param title: 标题
        :param list_: 版本信息列表
        :param len_:  版本信息列表长度
        :return: 版本信息
        """

        current_page = 1

        if int(len_ % self.__page_size) == 0:
            page_count = int(len_ / self.__page_size)
        else:
            page_count = int(len_ / self.__page_size) + 1

        regx = re.compile("(^\\d{1,%d})+P$" % len(str(page_count)))

        while True:
            Helper.cmd_clean()

            start_index = (current_page - 1) * self.__page_size
            if current_page == page_count:
                end_index = start_index + len_
            else:
                end_index = start_index + self.__page_size

            _list = list_[start_index:end_index]

            table = prettytable.PrettyTable()
            table.title = title
            table.field_names = ["编号", "软件包", "版本号", "发布时间"]

            for i, item in enumerate(_list):
                table.add_row([start_index + i + 1, item.name, item.version, item.datetime])

            print(table)
            print("['W'上一页|'S'下一页|'A'首页|'D'末页|'[n]P'页|第%d页-共%d页]" % (current_page, page_count))

            input_id = (input("请输入编号：") or "0").upper()

            if input_id == "A":
                current_page = 1
                continue

            if input_id == "D":
                current_page = page_count
                continue

            if input_id == "W":
                if current_page > 1:
                    current_page = current_page - 1
                continue

            if input_id == "S":
                if current_page < page_count:
                    current_page = current_page + 1
                continue

            if regx.match(input_id):
                page_no = int(regx.findall(input_id)[0])
                if page_no > page_count:
                    current_page = page_count
                elif page_no < 1:
                    current_page = 1
                else:
                    current_page = page_no
                continue

            input_id = (lambda n: int(n) if n.isdigit() else -1)(input_id)

            if input_id > len_ or input_id < 1:
                Helper.print_warn("您的输入有误！")
                time.sleep(1)
            else:
                return list_[input_id - 1]

    @staticmethod
    def __all(title: str, list_: list[VersionInfo], len_: int) -> VersionInfo:
        """
        将版本信息列表数据一次性全部处理

        :param title: 标题
        :param list_: 版本信息列表
        :param len_: 版本信息列表长度
        :return: 版本信息
        """

        table = prettytable.PrettyTable()
        table.title = title
        table.field_names = ["编号", "软件包", "版本号", "发布时间"]

        for i, item in enumerate(list_):
            table.add_row([i + 1, item.name, item.version, item.datetime])

        while True:
            Helper.cmd_clean()
            print(table)

            input_id = (lambda n: int(n) if n.isdigit() else -1)(input("请输入编号：") or "0")

            if input_id > len_ or input_id < 1:
                Helper.print_warn("您的输入有误！")
                time.sleep(1)
            else:
                return list_[input_id - 1]

    @staticmethod
    def __get_version_list(url: str, pkg_prefix: str, pkg_suffix: str) -> list[VersionInfo]:
        """
        获取版本清单

        注意：pkg_prefix + {version} + pkg_suffix，为软件包全称

        :param url: Apache档案地址
        :param pkg_prefix: 软件包前缀
        :param pkg_suffix: 软件包后缀
        :return: 版本信息列表
        """

        try:
            resp = requests.get(url)
            html = resp.text

            result = Archive.regex_html.findall(html)

            if len(result) == 0:
                raise Exception("正则提取失败，提取结果：%s条" % len(result))

            result_list = []
            for e in result:
                item = VersionInfo()
                item.name = pkg_prefix + e[0] + pkg_suffix
                item.version = e[0]
                item.datetime = e[1]
                result_list.append(item)

            return result_list

        except Exception as e:
            Helper.print_error("⛔错误：解析Apache archive异常！%s" % e)
            traceback.print_exc()
            exit()

    def select(self) -> list[VersionInfo]:
        """
        选择版本

        :return: 版本信息列表
        """

        def task() -> None:
            """
            任务函数

            :return: None
            """

            future_rocketmq = Context.executor.submit(self.__get_version_list, const.APACHE_ROCKETMQ_URL,
                                                      const.APACHE_ROCKETMQ_PREFIX,
                                                      const.APACHE_ROCKETMQ_SUFFIX)
            future_console = Context.executor.submit(self.__get_version_list,
                                                     const.APACHE_ROCKETMQ_CONSOLE_URL,
                                                     const.APACHE_ROCKETMQ_CONSOLE_PREFIX,
                                                     const.APACHE_ROCKETMQ_CONSOLE_SUFFIX)

            while True:
                if future_rocketmq.done() and future_console.done():
                    self.__rocketmq_list = future_rocketmq.result()
                    self.__console_list = future_console.result()
                    break
                else:
                    time.sleep(.1)

        Helper.progress("解析版本库", task)

        while True:
            rocketmq_version = self.__select("RocketMQ版本清单", self.__rocketmq_list)
            console_version = self.__select("Console版本清单", self.__console_list)

            table = prettytable.PrettyTable()
            table.title = "确认清单"
            table.field_names = ["编号", "软件包", "版本号", "发布时间"]

            for i, item in enumerate([rocketmq_version, console_version]):
                table.add_row([i + 1, item.name, item.version, item.datetime])

            Helper.cmd_clean()
            print(table)

            input_id = (input("确认无误['Y'是|'N'否]：") or "Y").upper()

            if input_id == "Y":
                break
            else:
                continue

        return [rocketmq_version, console_version]
