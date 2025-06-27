# coding:utf-8
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QLinearGradient
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon
from HOIModEditor.main.common.config import LIBRARY_URL, GITHUB_URL
from HOIModEditor.main.components.link_card import LinkCardView
from HOIModEditor.main.components.sample_card import SampleCardView
from HOIModEditor.main.common.style_sheet import StyleSheet


class BannerWidget(QWidget):
    """Banner widget"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(343)
        self.vBoxLayout = QVBoxLayout(self)

        self.galleryLabel = QLabel('主页', self)
        self.galleryLabel.setObjectName('galleryLabel')
        self.galleryLabel.setFont(QApplication.font())

        self.banner = QPixmap('HOIModEditor/main/resource/images/header.png')
        self.linkCardView = LinkCardView(self)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignmentFlag.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.linkCardView.addCard(
            'HOIModEditor/main/resource/images/logo.png',
            self.tr('霜泽图书馆'),
            self.tr('这是一个专注于《钢铁雄心4》模组开发的社区'),
            LIBRARY_URL
        )
        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('GitHub'),
            self.tr('访问图书馆的GitHub页面'),
            GITHUB_URL
        )

        # 用于缓存尺寸相关的对象，避免每次重绘都重新计算
        self._cached_path = None
        self._cached_gradient = None
        self._scaled_banner = None

    def resizeEvent(self, event):
        """窗口尺寸变化时重新计算缓存的 QPixmap、路径和渐变"""
        super().resizeEvent(event)
        w, h = self.width(), self.height()

        # 缓存缩放后的图片
        self._scaled_banner = self.banner.scaled(
            self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # 构造路径
        path = QPainterPath()
        path.setFillRule(Qt.FillRule.WindingFill)
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        self._cached_path = path.simplified()

        # 构造渐变
        gradient = QLinearGradient(0, 0, 0, h)
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))
        self._cached_gradient = gradient

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        # 如果缓存为空（例如首次绘制时），则调用 resizeEvent 进行初始化
        if self._cached_path is None or self._cached_gradient is None or self._scaled_banner is None:
            self.resizeEvent(e)

        # 绘制渐变背景
        painter.fillPath(self._cached_path, QBrush(self._cached_gradient))
        # 绘制图片（利用缓存的缩放图）
        painter.fillPath(self._cached_path, QBrush(self._scaled_banner))


class HomeInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def loadSamples(self):
        mods = SampleCardView(self.tr("导航"), self.view)
        """
        mods.addSampleCard(
            icon=":/gallery/images/controls/Button.png",
            title="管理Mod",
            content=self.tr("A control that responds to user input and emit clicked signal."),
            routeKey="CreateModsInterface",
            index=0
        )
        """
        self.vBoxLayout.addWidget(mods)
