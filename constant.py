import os

import helper
from commons import const

const.TARGET_HOME = helper.get_current_work_dir() + os.sep + "target"
const.ASSET_HOME = const.TARGET_HOME + os.sep + "asset"
const.DIST_HOME = const.TARGET_HOME + os.sep + "dist"

const.ASSET_MAVEN_HOME = const.ASSET_HOME + os.sep + "maven"
const.ASSET_MAVEN_SETTING_XML = const.ASSET_MAVEN_HOME + os.sep + "settings.xml"
const.ASSET_MAVEN_SETTING_REPO_FLAG = "{MAVEN_REPO}"

const.MAVEN_HOME = const.TARGET_HOME + os.sep + "maven"
const.MAVEN_REPO = const.MAVEN_HOME + os.sep + "repo"
const.MAVEN_CONF = const.MAVEN_HOME + os.sep + "conf"
const.MAVEN_SETTING_XML = const.MAVEN_CONF + os.sep + "settings.xml"
