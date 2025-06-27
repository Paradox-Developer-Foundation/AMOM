# coding:utf-8
import sys
from qfluentwidgets import qconfig, QConfig, ConfigItem, BoolValidator, Theme, FolderValidator


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """ Config of application """

    gameFolder = ConfigItem(
        "Folders", "GameFolder", "", FolderValidator())

    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    steamLaunchEnabled = ConfigItem("MainWindow", "LaunchModeEnabled", "", BoolValidator())

THIS_YEAR = 2025
VERSION = "0.2.34"
LIBRARY_URL = "https://docs.szlib.eu"
GITHUB_URL = "https://github.com/jingzhouzhidi/QIUQI-LIBRARY"
LOVER = "ddd"

cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('HOIModEditor/main/config/config.json', cfg)