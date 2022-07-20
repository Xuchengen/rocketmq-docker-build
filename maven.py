import os.path
import pathlib
import shutil
import zipfile

import downloader
from constant import const
from helper import Helper


class Maven(object):
    """
    Maven
    """

    @staticmethod
    def __install() -> None:
        """
        安装Maven

        :return: None
        """

        path_dist = pathlib.Path(const.DIST_HOME)
        path_maven_pkg = path_dist.joinpath(const.APACHE_MAVEN_BIN_NAME)

        if path_maven_pkg.exists():
            path_maven = pathlib.Path(const.MAVEN_HOME)

            # 删除已有maven环境
            if path_maven.exists():
                path_maven.chmod(0o777)
                shutil.rmtree(path_maven)

            # 解压到目录
            zip_file = zipfile.ZipFile(path_maven_pkg)

            for f in zip_file.namelist():
                zip_file.extract(f, const.TOOLS_HOME)
            zip_file.close()

            # 修改目录名称为maven
            for f in path_maven.parent.iterdir():
                if f.name == const.APACHE_MAVEN_VERSION:
                    f.rename(path_maven)
                    break

            # 设置配置文件
            setting_xml_str = pathlib.Path(const.ASSET_MAVEN_SETTING_XML).read_text(encoding="utf8") \
                .replace(const.ASSET_MAVEN_SETTING_REPO_FLAG, const.MAVEN_REPO)

            # 写配置文件
            pathlib.Path(const.MAVEN_SETTING_XML).write_text(setting_xml_str)

            # 创建仓库目录
            pathlib.Path(const.MAVEN_REPO).mkdir()

            # 设置环境变量
            os.environ["MAVEN_HOME"] = const.MAVEN_HOME
            os.environ["Path"] = os.environ["Path"] + os.pathsep + str(path_maven.joinpath("bin"))

        else:

            # 下载apache maven
            download = downloader.Downloader(const.APACHE_MAVEN_URL, const.DIST_HOME)
            download.download()

            # 安装
            Maven.__install()

    @staticmethod
    def install():
        Helper.progress("安装maven", Maven.__install)
