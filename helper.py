import os

import shutil


# 获取当前执行目录
def get_current_work_dir() -> str:
    return os.getcwd()


# 操作系统支持javac命令
def is_os_support_java() -> bool:
    return _is_os_tool("java")


# 操作系统支持javac命令
def is_os_support_javac() -> bool:
    return _is_os_tool("javac")


# 操作系统支持mvn命令
def is_os_support_mvn() -> bool:
    return _is_os_tool("mvn")


# 操作系统支持docker命令
def is_os_support_docker() -> bool:
    return _is_os_tool("docker")


# 操作系统支持命令工具
def _is_os_tool(cmd_tool_name: str) -> bool:
    return shutil.which(cmd_tool_name) is not None
