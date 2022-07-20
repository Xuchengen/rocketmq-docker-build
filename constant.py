import os

from commons import const
from helper import Helper

const.APACHE_ROCKETMQ_PREFIX = "rocketmq-all-"
const.APACHE_ROCKETMQ_SUFFIX = "-bin-release.zip"
const.APACHE_ROCKETMQ_URL = "https://archive.apache.org/dist/rocketmq"
const.APACHE_ROCKETMQ_BASE_URL = const.APACHE_ROCKETMQ_URL \
                                 + "/{version}/" + const.APACHE_ROCKETMQ_PREFIX \
                                 + "{version}" + const.APACHE_ROCKETMQ_SUFFIX

const.APACHE_ROCKETMQ_CONSOLE_PREFIX = "rocketmq-dashboard-"
const.APACHE_ROCKETMQ_CONSOLE_SUFFIX = "-source-release.zip"
const.APACHE_ROCKETMQ_CONSOLE_URL = "https://archive.apache.org/dist/rocketmq/rocketmq-dashboard/"
const.APACHE_ROCKETMQ_CONSOLE_BASE_URL = const.APACHE_ROCKETMQ_CONSOLE_URL \
                                         + "/{version}/" + const.APACHE_ROCKETMQ_CONSOLE_PREFIX \
                                         + "{version}" + const.APACHE_ROCKETMQ_CONSOLE_SUFFIX

const.APACHE_MAVEN_VERSION = "apache-maven-3.8.6"
const.APACHE_MAVEN_BIN_NAME = const.APACHE_MAVEN_VERSION + "-bin.zip"
const.APACHE_MAVEN_URL = "https://archive.apache.org/dist/maven/maven-3/3.8.6/binaries/" + const.APACHE_MAVEN_BIN_NAME

const.TARGET_HOME = Helper.get_current_work_dir() + os.sep + "target"
const.ASSET_HOME = const.TARGET_HOME + os.sep + "asset"
const.DIST_HOME = const.TARGET_HOME + os.sep + "dist"
const.TOOLS_HOME = const.TARGET_HOME + os.sep + "tools"
const.BUILD_HOME = const.TARGET_HOME + os.sep + "build"
const.MAKE_HOME = const.TARGET_HOME + os.sep + "make"

const.ASSET_MAVEN_HOME = const.ASSET_HOME + os.sep + "maven"
const.ASSET_MAVEN_SETTING_XML = const.ASSET_MAVEN_HOME + os.sep + "settings.xml"
const.ASSET_MAVEN_SETTING_REPO_FLAG = "{MAVEN_REPO}"

const.ASSET_DOCKER_HOME = const.ASSET_HOME + os.sep + "docker"
const.ASSET_ROCKETMQ_HOME = const.ASSET_HOME + os.sep + "rocketmq"
const.ASSET_CONSOLE_HOME = const.ASSET_HOME + os.sep + "console"

const.MAVEN_HOME = const.TOOLS_HOME + os.sep + "maven"
const.MAVEN_REPO = const.MAVEN_HOME + os.sep + "repo"
const.MAVEN_CONF = const.MAVEN_HOME + os.sep + "conf"
const.MAVEN_SETTING_XML = const.MAVEN_CONF + os.sep + "settings.xml"
