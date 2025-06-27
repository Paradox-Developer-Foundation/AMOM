# coding:utf-8
from PyQt6.QtCore import Qt, QUrl, QEvent
from PyQt6.QtGui import QDesktopServices, QPainter, QPen, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame
from qfluentwidgets import ScrollArea, isDarkTheme, TitleLabel, CaptionLabel, StrongBodyLabel
from HOIModEditor.main.common.style_sheet import StyleSheet


class SeparatorWidget(QWidget):
    """ Seperator widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(6, 16)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(1)
        pen.setCosmetic(True)
        c = QColor(255, 255, 255, 21) if isDarkTheme() else QColor(0, 0, 0, 15)
        pen.setColor(c)
        painter.setPen(pen)

        x = self.width() // 2
        painter.drawLine(x, 0, x, self.height())


class ToolBar(QWidget):

    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = TitleLabel(title, self)
        self.subtitleLabel = CaptionLabel(subtitle, self)

        self.vBoxLayout = QVBoxLayout(self)

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(84)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 22, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.subtitleLabel.setTextColor(QColor(96, 96, 96), QColor(216, 216, 216))


class ExampleCard(QWidget):
    """ Example card """

    def __init__(self, title, widget: QWidget, stretch=0, parent=None):
        super().__init__(parent=parent)
        self.widget = widget
        self.stretch = stretch

        self.titleLabel = StrongBodyLabel(title, self)
        self.card = QFrame(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QVBoxLayout(self.card)
        self.topLayout = QHBoxLayout()

        self.__initWidget()

    def __initWidget(self):
        self.__initLayout()
        self.card.setObjectName('card')

    def __initLayout(self):
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        self.cardLayout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        self.topLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)

        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setContentsMargins(12, 12, 12, 12)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.card, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.cardLayout.setSpacing(0)
        self.cardLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cardLayout.addLayout(self.topLayout, 0)

        self.widget.setParent(self.card)
        self.topLayout.addWidget(self.widget)
        if self.stretch == 0:
            self.topLayout.addStretch(1)

        self.widget.show()

    def eventFilter(self, obj, e):
        if obj is self.sourceWidget:
            if e.type() == QEvent.Type.MouseButtonRelease:
                QDesktopServices.openUrl(QUrl(self.sourcePath))

        return super().eventFilter(obj, e)


class GalleryInterface(ScrollArea):

    def __init__(self, title: str, subtitle: str, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.toolBar = ToolBar(title, subtitle, self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

        self.view.setObjectName('view')
        StyleSheet.GALLERY_INTERFACE.apply(self)

    def addExampleCard(self, title, widget, stretch=0):
        card = ExampleCard(title, widget, stretch, self.view)
        self.vBoxLayout.addWidget(card, 0, Qt.AlignmentFlag.AlignTop)
        return card

    def scrollToCard(self, index: int):
        """ scroll to example card """
        w = self.vBoxLayout.itemAt(index).widget()
        self.verticalScrollBar().setValue(w.y())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.toolBar.resize(self.width(), self.toolBar.height())

