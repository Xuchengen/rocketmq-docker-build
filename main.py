import pathlib
import zipfile

import constant
import downloader


def main():
    version = "apache-maven-3.8.6"
    url = "https://archive.apache.org/dist/maven/maven-3/3.8.6/binaries/apache-maven-3.8.6-bin.zip"
    download_maven = downloader.Downloader(url, constant.const.DIST_HOME)
    download_maven.download()

    download_maven_file = download_maven.target_file

    path = pathlib.Path(constant.const.MAVEN_HOME)
    if path.exists():
        path.rmdir()

    zip_file = zipfile.ZipFile(download_maven_file)

    for f in zip_file.namelist():
        zip_file.extract(f, path.parent)
    zip_file.close()

    # 修改为maven
    for f in list(path.parent.iterdir()):
        if f.name == version:
            f.rename(constant.const.MAVEN_HOME)

    # 设置权限
    pathlib.Path(constant.const.MAVEN_HOME).chmod(777)

    # 模板替换
    setting_xml_str = pathlib.Path(constant.const.ASSET_MAVEN_SETTING_XML).read_text(encoding="utf8") \
        .replace(constant.const.ASSET_MAVEN_SETTING_REPO_FLAG, constant.const.MAVEN_REPO)

    # 写到文件
    pathlib.Path(constant.const.MAVEN_SETTING_XML).write_text(setting_xml_str)

    # 创建目录
    pathlib.Path(constant.const.MAVEN_REPO).mkdir()


if __name__ == '__main__':
    main()
