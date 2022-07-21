import signal
from typing import Any

import archive
from archive import VersionInfo
from builder import Builder
from helper import Helper
from maven import Maven


def main():
    app_env_check()

    while True:

        list_version = archive.Archive(page_size=10).select()

        tag = (input("请输入镜像标签：") or "test/rocketmq:%s" % list_version[0].version)

        result = Helper.progress("构建镜像", task_build, tag, list_version)

        if result is not None and not result[0]:
            Helper.print_error("😂看起来好像出错了!\n%s" % result[1])
            exit()

        print("🔥构建成功,镜像标签为：%s" % tag)

        input_id = (input("继续构建['Y'是|'N'否]：") or "Y").upper()

        if input_id == "Y":
            continue
        else:
            gameover()
            break


def task_build(tag: str, list_version: list[VersionInfo]) -> Any:
    """
    构建任务

    :param tag: Docker Tag 例如：仓库/应用:版本号 -> xce/rocketmq:4.9.4
    :param list_version: 版本信息列表
    :return: 返回值不确定
    """

    result_console = Builder.build_console(list_version[1].version)

    # 把错误往上抛
    if result_console is not None and not result_console[0]:
        return result_console

    Builder.build_rocketmq(list_version[0].version)

    result_docker = Builder.build_docker(tag, list_version[0].version, list_version[1].version)

    # 把错误往上抛
    if result_docker is not None and not result_docker[0]:
        return result_docker


def app_env_check() -> None:
    """
    应用环境检测

    :return: None
    """
    if not (Helper.is_os_support_java() and Helper.is_os_support_javac()):
        Helper.print_error("⛔错误：当前操作系统没有JDK环境，请安装JDK并设置好环境变量！")
        exit()

    if not Helper.is_os_support_docker():
        Helper.print_error("⛔错误：当前操作系统没有Docker环境，请安装Docker并RUN起来！")
        exit()
    else:
        if not Helper.is_docker_runing():
            Helper.print_error("⛔错误：Docker似乎没有RUN起来啊！")
            exit()

    if not Helper.is_os_support_mvn():
        Helper.print_warn("⚠️警告：当前操作系统没有Maven环境，本程序将初始化一个内置Maven环境！")
        Maven.install()


def signal_handler(signum, frame):
    """
    信号处理

    :param signum:
    :param frame:
    :return:
    """
    if signum == signal.SIGINT.value:
        gameover()


def gameover():
    """
    游戏结束

    :return: None
    """
    print("\n❤️感谢您的使用，我们下次再见！")
    exit()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
