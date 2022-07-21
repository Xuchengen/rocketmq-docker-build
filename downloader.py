import os
import traceback
import urllib

import requests

from helper import Helper


class Downloader(object):
    """
    下载者
    """

    def __init__(self, url: str, target_file: str):
        """
        构造方法

        :param url: 下载地址
        :param target_file: 存储目标路径
        """

        self.url = url
        # 下载文件前先请求一下响应头
        self.__header_resp = requests.head(url, allow_redirects=True)
        self.file_name = self.__get_file_name()
        self.file_size = self.__get_file_size()
        self.target_file = target_file + self.file_name if str(target_file).endswith(
            os.sep) else target_file + os.sep + self.file_name

    def __get_file_name(self) -> str:
        """
        获取文件名

        :return: 文件名称字符串
        """

        file_name = None
        if 'Content-Disposition' in self.__header_resp.headers:
            name = self.__header_resp.headers.get('Content-Disposition').split('name=')[1]
            file_name = urllib.parse.unquote(name, encoding='utf8')
        elif os.path.splitext(self.__header_resp.url)[1] != '':
            file_name = os.path.basename(self.__header_resp.url)
        return file_name

    def __get_file_size(self) -> int:
        """
        获取文件大小（字节数）

        :return: 文件大小（字节数）
        """

        try:
            return int(self.__header_resp.headers['Content-Length'])
        except Exception as e:
            Helper.print_error('⛔错误：获取文件大小异常！%s' % e)
            traceback.print_exc()
            exit()

    def __download_file(self) -> None:
        """
        下载文件

        :return:  None
        """

        if os.path.exists(self.target_file):
            os.remove(self.target_file)

        resp = requests.get(self.url, stream=True)

        with open(self.target_file, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    def download(self) -> None:
        """
        下载

        :return: None
        """

        self.__download_file()
