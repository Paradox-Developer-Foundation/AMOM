# coding: utf-8
import os
import subprocess

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import (NavigationItemPosition, FluentWindow,
                            SplashScreen, SystemThemeListener, isDarkTheme)
from qfluentwidgets import FluentIcon
from HOIModEditor.main.view.gallery_interface import GalleryInterface
from HOIModEditor.main.view.home_interface import HomeInterface
from HOIModEditor.main.view.local_mods_interface import LocalModsInterface
from HOIModEditor.main.view.create_mod_interface import CreateModInterface
from HOIModEditor.main.view.setting_interface import SettingInterface
from HOIModEditor.main.common.config import cfg
from HOIModEditor.main.common.signal_bus import signalBus
from HOIModEditor.main.common import resource #不要删除此import！即使标记为无效！


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

        self.themeListener = SystemThemeListener(self)
        self.themeListener.start()

        self.homeInterface = HomeInterface(self)
        self.createModInterface = CreateModInterface(self)
        self.LocalModsInterface = LocalModsInterface(self)
        self.navigationInterface.addItem(
            routeKey='Launch Game',
            icon=FluentIcon.PLAY,
            text="启动游戏",
            onClick=self.launch_game,
            selectable=False,
            tooltip="启动游戏",
            position=NavigationItemPosition.BOTTOM
        )
        self.settingInterface = SettingInterface(self)

        self.connectSignalToSlot()

        self.initNavigation()
        self.splashScreen.finish()

        self.navigationInterface.setExpandWidth(160)
        self.setUpdatesEnabled(True)

        self._galleryInterfaceDict = {}

    def initWindow(self):
        self.resize(1280, 960)
        self.setWindowIcon(QIcon('HOIModEditor/main/resource/images/icon.png'))
        self.setWindowTitle('钢铁雄心Mod编辑器')
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(150, 150))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()

        self._adjustTitleBar()
        QApplication.processEvents()

    def _adjustTitleBar(self):
        titleBar = getattr(self, 'titleBar', None)
        layout = titleBar.layout()
        margins = layout.contentsMargins()
        layout.setContentsMargins(margins.left() - 2, margins.top(),
                                  margins.right(), margins.bottom())
        titleBar.iconLabel.move(titleBar.iconLabel.x() - 2, titleBar.iconLabel.y())
        titleBar.titleLabel.move(titleBar.titleLabel.x() - 2, titleBar.titleLabel.y())

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, self.tr('主页'))
        self.addSubInterface(self.createModInterface, FluentIcon.ADD, self.tr('Mod创建'))
        self.addSubInterface(self.LocalModsInterface, FluentIcon.BOOK_SHELF, self.tr('Mod列表'))
        self.navigationInterface.addSeparator()

        self.addSubInterface(
            self.settingInterface, FluentIcon.SETTING, self.tr('设置'), NavigationItemPosition.BOTTOM
        )

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.splashScreen.resize(self.size())

    def closeEvent(self, e):
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)

    def _onThemeChangedFinished(self):
        super()._onThemeChangedFinished()
        if self.isMicaEffectEnabled():
            QTimer.singleShot(100, lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()))

    def switchToSample(self):
        """切换到指定 sample 页面"""
        if not self._galleryInterfaceDict:
            self._galleryInterfaceDict = {
                w.objectName(): w for w in self.findChildren(GalleryInterface)
            }

    def launch_game(self):
        if not cfg.get(cfg.steamLaunchEnabled):
            subprocess.run([f"{cfg.get(cfg.gameFolder)}/dowser.exe", "-debug"])
        else:
            os.startfile("steam://rungameid/394360")