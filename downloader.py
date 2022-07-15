import os
import threading
import time
import traceback
import urllib

import requests


class Downloader:

    # 构造方法
    def __init__(self, url: str, target_file: str):
        self.url = url
        # 下载文件前先请求一下响应头
        self.__header_resp = requests.head(url, allow_redirects=True)
        self.file_name = self.__get_file_name()
        self.file_size = self.__get_file_size()
        self.target_file = target_file + self.file_name if str(target_file).endswith(
            os.sep) else target_file + os.sep + self.file_name

    # 获取文件名
    def __get_file_name(self):
        file_name = None
        if 'Content-Disposition' in self.__header_resp.headers:
            name = self.__header_resp.headers.get('Content-Disposition').split('name=')[1]
            file_name = urllib.parse.unquote(name, encoding='utf8')
        elif os.path.splitext(self.__header_resp.url)[1] != '':
            file_name = os.path.basename(self.__header_resp.url)
        return file_name

    # 获取文件大小（字节数）
    def __get_file_size(self):
        try:
            return int(self.__header_resp.headers['Content-Length'])
        except Exception as e:
            print('错误：获取文件大小异常！%s' % e)
            traceback.print_exc()
            exit()

    # 下载文件
    def __download_file(self):
        if os.path.exists(self.target_file):
            os.remove(self.target_file)

        resp = requests.get(self.url, stream=True)

        with open(self.target_file, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    # 下载进度
    def __download_progress(self):
        # 临时已下载文件大小
        temp_file_size = 0

        while temp_file_size < self.file_size:
            time.sleep(1)

            if os.path.exists(self.target_file):
                history_temp_file_size = temp_file_size
                temp_file_size = os.path.getsize(self.target_file)
                speed = int((temp_file_size - history_temp_file_size) / 1024 / 1024)
                download_time = 0
                if speed != 0:
                    download_time = int((self.file_size - temp_file_size) / 1024 / 1024 / speed)

                # 比例
                rate = temp_file_size / self.file_size
                # 百分比
                rate_num = int(rate * 100)
                # 掩码个数
                mask_number = int(50 * rate)
                template = '[下载进度]:[\033[31m%s%s\033[0m]%d%% 网速：%d MB/s 剩余：%d 秒'
                out = template % ("#" * mask_number, " " * (50 - mask_number), rate_num, speed, download_time)
                print('\r' + out, end=' ')

    # 下载
    def download(self):
        print("文件名称：" + self.file_name)
        print('文件大小：%.2f' % (self.file_size / 1024 / 1024) + "MB")
        print("下载路径：" + self.target_file)
        thread = threading.Thread(target=self.__download_file)
        thread.start()
        self.__download_progress()
