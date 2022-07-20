import signal
import sys

import archive
from archive import VersionInfo
from builder import Builder
from helper import Helper
from maven import Maven


def main():
    if not (Helper.is_os_support_java() and Helper.is_os_support_javac()):
        Helper.print_error("错误：当前操作系统没有JDK环境，请安装JDK并设置好环境变量！")
        exit()

    if not Helper.is_os_support_docker():
        Helper.print_error("错误：当前操作系统没有Docker环境，请安装Docker并RUN起来！")
        exit()
    else:
        if not Helper.is_docker_runing():
            Helper.print_error("错误：Docker似乎没有RUN起来啊！")
            exit()

    if not Helper.is_os_support_mvn():
        Helper.print_warn("警告：当前操作系统没有Maven环境，本程序将初始化一个内置Maven环境！")
        Maven.install()

    list_version = archive.Archive(page_size=10).select()

    Helper.progress("构建", task, list_version)


def task(list_version: list[VersionInfo]):
    Builder.build_console(list_version[1].version)
    Builder.build_rocketmq(list_version[0].version)
    Builder.build_docker(list_version[0].version, list_version[1].version)


# 信号处理
def signal_handler(signum, frame):
    if signum == signal.SIGINT.value:
        print("\n感谢您的使用，我们下次再见！")
        sys.exit(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
