import os
import pathlib
import shutil
import zipfile

import downloader
from constant import const
from helper import Helper


class Builder(object):
    """
    构建者
    """

    @staticmethod
    def build_console(version: str) -> list[bool | str]:
        """
        构建Console

        :param version: Console版本号
        :return: None
        """

        path_console = pathlib.Path(const.BUILD_HOME).joinpath(const.APACHE_ROCKETMQ_CONSOLE_PREFIX + version)

        # 判断版本目录是否存在
        if path_console.exists():

            # 设置权限
            path_console.chmod(0o777)

            path_jar = path_console.joinpath("target").joinpath(const.APACHE_ROCKETMQ_CONSOLE_PREFIX + version + ".jar")

            # 判断Jar是否存在
            if not path_jar.exists():
                # 编译
                # JVM环境变量JAVA_TOOLS_OPTIONS

                cmd = "mvn package -Dfile.encoding=UTF8 -Dmaven.test.skip=true -file \"%s\" 2>&1" \
                      % (path_console.joinpath("pom.xml"))

                result = Helper.shell(cmd)

                if "BUILD SUCCESS" in result:
                    return [True, result]
                else:
                    return [False, result]
        else:

            path_zip = pathlib.Path(const.DIST_HOME) \
                .joinpath(const.APACHE_ROCKETMQ_CONSOLE_PREFIX + version + const.APACHE_ROCKETMQ_CONSOLE_SUFFIX)

            # 判断源码包是否存在
            if path_zip.exists():

                # 解压
                zip_file = zipfile.ZipFile(path_zip)

                for f in zip_file.namelist():
                    zip_file.extract(f, const.BUILD_HOME)
                zip_file.close()

                # 设置权限
                path_console.chmod(0o777)

                # 构建
                Builder.build_console(version)

            else:

                # 下载源码包
                url = str(const.APACHE_ROCKETMQ_CONSOLE_BASE_URL).replace("{version}", version)
                download_console = downloader.Downloader(url, const.DIST_HOME)
                download_console.download()

                # 构建
                Builder.build_console(version)

    @staticmethod
    def build_rocketmq(version: str) -> None:
        """
        构建Rocketmq

        :param version: Rocketmq版本号
        :return: None
        """

        path_str = const.BUILD_HOME + os.sep + const.APACHE_ROCKETMQ_PREFIX + version

        # 判断版本目录不存在
        if not os.path.exists(path_str):

            package = const.DIST_HOME + os.sep + \
                      const.APACHE_ROCKETMQ_PREFIX + \
                      version + const.APACHE_ROCKETMQ_SUFFIX

            # 判断源码包是否存在
            if os.path.exists(package):

                # 创建目录
                os.mkdir(path_str)

                # 解压到目录
                zip_file = zipfile.ZipFile(package)

                for f in zip_file.namelist():
                    zip_file.extract(f, path_str)
                zip_file.close()

                path = pathlib.Path(path_str)

                if len(list(path.iterdir())) == 1:
                    for f in path.iterdir():
                        for sf in f.iterdir():
                            sf.replace(f.parent.joinpath(sf.name))
                        f.rmdir()
                        break

                # 设置权限
                os.chmod(path_str, 0o777)

            else:

                # 下载源码包
                url = str(const.APACHE_ROCKETMQ_BASE_URL).replace("{version}", version)
                download_rocketmq = downloader.Downloader(url, const.DIST_HOME)
                download_rocketmq.download()

                # 构建
                Builder.build_rocketmq(version)

    @staticmethod
    def build_docker(tag: str, rocketmq_version: str, console_version: str) -> list[bool | str]:
        """
        制作镜像

        :param tag: 标签名称
        :param rocketmq_version: Rocketmq版本号
        :param console_version: Console版本号
        :return: None
        """

        path_rocketmq = pathlib.Path(const.BUILD_HOME) \
            .joinpath(const.APACHE_ROCKETMQ_PREFIX + rocketmq_version)

        path_console_jar = pathlib.Path(const.BUILD_HOME) \
            .joinpath(const.APACHE_ROCKETMQ_CONSOLE_PREFIX + console_version) \
            .joinpath("target").joinpath(const.APACHE_ROCKETMQ_CONSOLE_PREFIX + console_version + ".jar")

        path_make = pathlib.Path(const.MAKE_HOME)

        path_make_version = path_make.joinpath(rocketmq_version)

        # 删除make目录
        if path_make.exists():
            path_make.chmod(0o777)
            shutil.rmtree(path_make)

        # 创建目录
        path_make.mkdir()
        path_make.chmod(0o777)

        # 创建版本目录
        path_make_version.mkdir()

        # 放入Dockerfile及脚本
        for f in pathlib.Path(const.ASSET_DOCKER_HOME).iterdir():
            if f.name == "Dockerfile":
                shutil.copyfile(f, path_make.joinpath(f.name))
            else:
                shutil.copyfile(f, path_make_version.joinpath(f.name))

        # 放入rocketmq
        path_make_rocketmq = path_make_version.joinpath("rocketmq")
        shutil.copytree(path_rocketmq, path_make_rocketmq)

        # 放入rocketmq脚本
        for f in pathlib.Path(const.ASSET_ROCKETMQ_HOME).iterdir():
            shutil.copyfile(f, path_make_rocketmq.joinpath("bin").joinpath(f.name))

        # 放入rocketmq-console
        path_make_console = path_make_version.joinpath("console")
        path_make_console_store = path_make_console.joinpath("store")
        path_make_console_config = path_make_console.joinpath("config")
        path_make_console.mkdir()
        path_make_console_store.mkdir()
        path_make_console_config.mkdir()
        shutil.copyfile(path_console_jar, path_make_console.joinpath("rocketmq-console.jar"))

        # 放入rocketmq-console配置文件
        for f in pathlib.Path(const.ASSET_CONSOLE_HOME).iterdir():
            if f.name == "users.properties":
                shutil.copyfile(f, path_make_console_store.joinpath(f.name))
            else:
                shutil.copyfile(f, path_make_console_config.joinpath(f.name))

        # 创建data目录为volume做准备
        path_make_data = path_make_version.joinpath("data")
        path_make_data_logs = path_make_data.joinpath("logs")
        path_make_data_rocketmq = path_make_data.joinpath("rocketmq")
        path_make_data_rocketmq_store = path_make_data_rocketmq.joinpath("store")
        path_make_data_rocketmq_conf = path_make_data_rocketmq.joinpath("conf")
        path_make_data_console = path_make_data.joinpath("console")
        path_make_data_console_config = path_make_data_console.joinpath("config")
        path_make_data_console_store = path_make_data_console.joinpath("store")

        path_make_data_logs.mkdir(parents=True)
        path_make_data_rocketmq_store.mkdir(parents=True)
        path_make_data_console.mkdir(parents=True)

        # 把/rocketmq/conf目录移动到/data/rocketmq/conf
        path_make_rocketmq.joinpath("conf").replace(path_make_data_rocketmq_conf)

        # 把/console/config目录移动到/data/console/config
        path_make_console_config.replace(path_make_data_console_config)

        # 把/console/store目录移动到/data/console/store
        path_make_console_store.replace(path_make_data_console_store)

        # 构建
        cmd = 'cd %s & docker build --no-cache -t %s --build-arg version=%s . 2>&1' \
              % (path_make, tag, rocketmq_version)

        result = Helper.shell(cmd)

        inspect_str = Helper.shell("docker inspect %s 2>&1" % tag)

        if "RepoTags" in inspect_str and tag in inspect_str:
            return [True, result]
        else:
            return [False, result]
