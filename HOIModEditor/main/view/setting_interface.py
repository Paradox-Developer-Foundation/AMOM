# coding:utf-8
import sys
import os
from qfluentwidgets import (
    SettingCardGroup,
    SwitchSettingCard,
    MessageBox,
    PrimaryPushSettingCard,
    ScrollArea,
    ExpandLayout,
    CustomColorSettingCard,
    setTheme,
    setThemeColor,
    OptionsSettingCard,
    PushSettingCard,
    FluentIcon,
    PrimaryPushButton
)
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtWidgets import QWidget, QLabel, QFileDialog, QHBoxLayout, QVBoxLayout, QApplication
from main.common.config import cfg, VERSION, THIS_YEAR, isWin11
from main.common.signal_bus import signalBus
from main.common.style_sheet import StyleSheet


class SettingInterface(ScrollArea):
    """设置界面（子页面）"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.settingLabel = QLabel(self.tr("设置"), self)

        # 通用组
        self.generalGroup = SettingCardGroup(self.tr('通用'), self.scrollWidget)
        self.gamePathCard = PushSettingCard(
            self.tr('选择游戏文件夹'),
            FluentIcon.FOLDER,
            self.tr("游戏目录"),
            cfg.get(cfg.gameFolder),
            self.generalGroup
        )
        self.launchModeCard = SwitchSettingCard(
            FluentIcon.GAME,
            self.tr('从Steam开启游戏'),
            self.tr('通过Steam链接来启动游戏'),
            cfg.steamLaunchEnabled,
            self.generalGroup
        )

        # 个性化组
        self.personalGroup = SettingCardGroup(self.tr('个性化'), self.scrollWidget)
        self.micaCard = SwitchSettingCard(
            FluentIcon.TRANSPARENT,
            self.tr('Mica效果'),
            self.tr('窗口和表面开启Windows 11的Mica效果'),
            cfg.micaEnabled,
            self.personalGroup
        )
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FluentIcon.BRUSH,
            self.tr('应用主题'),
            self.tr("调整应用主题外观"),
            texts=[
                self.tr('浅色(Beta)'), self.tr('深色'), self.tr('系统默认')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FluentIcon.PALETTE,
            self.tr('主题色'),
            self.tr('调整应用主题色'),
            self.personalGroup
        )

        # 关于组
        self.aboutGroup = SettingCardGroup(self.tr('关于'), self.scrollWidget)
        self.aboutCard = PrimaryPushSettingCard(
            self.tr('查看最新变化'),
            FluentIcon.INFO,
            self.tr('应用信息'),
            self.tr('© 2023-') + f"{THIS_YEAR}" +
            self.tr(' 霜泽图书馆 Shuangze Lib. S.A. ') +
            self.tr('当前版本 ') + VERSION,
            self.aboutGroup
        )

        self.__initWidget()

    def __initWidget(self):
        # 设置页面基本属性
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # 初始化样式
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)
        self.micaCard.setEnabled(isWin11())

        # 创建重启按钮，使用 PrimaryPushButton 并添加图标 FluentIcon.UPDATE
        self.restartButton = PrimaryPushButton(self.tr("重启程序以更改设置"), self)
        self.restartButton.setIcon(FluentIcon.UPDATE)  # 为按钮添加图标
        self.restartButton.setFixedSize(220, 36)
        self.restartButton.setVisible(False)
        self.restartButton.clicked.connect(self.restartApplication)

        # 初始化布局和信号
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        # 添加各功能卡片到对应组
        self.generalGroup.addSettingCard(self.gamePathCard)
        self.generalGroup.addSettingCard(self.launchModeCard)

        self.personalGroup.addSettingCard(self.micaCard)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)

        self.aboutGroup.addSettingCard(self.aboutCard)

        # 将全部组加入整体布局中
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.generalGroup)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __connectSignalToSlot(self):
        """连接信号与槽函数"""
        # 个性化设置项：变更时显示重启按钮
        cfg.themeChanged.connect(setTheme)
        self.themeCard.optionChanged.connect(lambda index: self.onSettingChanged())
        self.themeColorCard.colorChanged.connect(lambda c: (setThemeColor(c), self.onSettingChanged()))
        self.micaCard.checkedChanged.connect(
            lambda checked: (signalBus.micaEnableChanged.emit(checked), self.onSettingChanged()))
        self.gamePathCard.clicked.connect(self.__onGameFolderCardClicked)
        self.launchModeCard.checkedChanged.connect(lambda _: self.onSettingChanged())

        # 关于项
        self.aboutCard.clicked.connect(self.showChanges)

    def showChanges(self):
        title = self.tr('最新变化')
        content = self.tr("")
        w = MessageBox(title, content, self.window())
        w.setContentCopyable(True)
        w.yesButton.setText("确定")
        w.cancelButton.setText("取消")
        if w.exec():
            print('Yes button pressed')
        else:
            print('Cancel button pressed')

    def __onGameFolderCardClicked(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.gameFolder) == folder:
            return
        cfg.set(cfg.gameFolder, folder)
        self.gamePathCard.setContent(folder)
        self.onSettingChanged()

    def onSettingChanged(self):
        """当设置项有改动时显示重启按钮"""
        self.restartButton.setVisible(True)

    def restartApplication(self):
        """使用 QProcess.startDetached 实现应用重启"""
        # 禁用按钮防止重复点击
        self.restartButton.setEnabled(False)
        print("正在重启程序...")
        print("sys.executable:", sys.executable)
        print("sys.argv:", sys.argv)
        print("Current working directory:", os.getcwd())
        # 尝试启动新的独立进程
        if QProcess.startDetached(sys.executable, sys.argv):
            # 新进程启动成功，退出当前进程
            QApplication.exit(0)
        else:
            print("重启程序失败")
            self.restartButton.setEnabled(True)

    def add_title_label(self, layout, text):
        """辅助方法：向指定布局添加标题标签"""
        title_label = QLabel(text)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

    def resizeEvent(self, event):
        """重写 resizeEvent 以使重启按钮始终显示在右上角"""
        super().resizeEvent(event)
        margin = 30
        btn_width = self.restartButton.width()
        self.restartButton.move(self.width() - btn_width - margin, margin)
