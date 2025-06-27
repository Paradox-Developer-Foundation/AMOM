import os
import re
import logging
import webbrowser
from pathlib import Path
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QThread, pyqtSignal, QObject
from PyQt6.QtGui import QPixmap, QWheelEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QScrollArea
from qfluentwidgets import CardWidget, PrimaryPushButton, PushButton, SearchLineEdit, IndeterminateProgressRing

# 配置日志
logging.basicConfig(level=logging.INFO)


class SmoothScrollArea(QScrollArea):
    """
    自定义滚动区域，通过拦截 wheelEvent 并使用 QPropertyAnimation
    对垂直滚动条进行动画补间，实现平滑滚动效果。
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_animation = None

    def wheelEvent(self, event: QWheelEvent):
        current_value = self.verticalScrollBar().value()
        delta = event.angleDelta().y()
        new_value = current_value - delta
        new_value = max(self.verticalScrollBar().minimum(), min(new_value, self.verticalScrollBar().maximum()))
        animation = QPropertyAnimation(self.verticalScrollBar(), b"value", self)
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.setStartValue(current_value)
        animation.setEndValue(new_value)
        animation.start()
        self._current_animation = animation
        event.accept()


class ModLoader(QObject):
    """
    工作线程中专门用于加载模组信息。解析所有 .mod 文件后通过 finished 信号返回模组列表。
    """
    finished = pyqtSignal(list)

    def __init__(self, mod_dir: Path, parent=None):
        super().__init__(parent)
        self.mod_dir = mod_dir

    def run(self):
        mods = []
        for mod_file in self.mod_dir.iterdir():
            if mod_file.suffix.lower() != ".mod":
                continue
            mod_info = self.parse_mod_file(mod_file)
            if mod_info:
                mods.append(mod_info)
        mods.sort(key=lambda x: x[0])
        self.finished.emit(mods)

    def parse_mod_file(self, mod_file: Path):
        try:
            content = mod_file.read_text(encoding="utf-8")
        except Exception as e:
            logging.error("读取模组文件 %s 时出错: %s", mod_file.name, e)
            return None

        match_path = re.search(r'(?<!replace_)path\s*=\s*"\s*([^"]+?)\s*"', content)
        if not match_path:
            logging.warning("文件 %s 中未找到模组路径", mod_file.name)
            return None
        folder_path = match_path.group(1).strip()
        if folder_path.startswith("mod/"):
            folder_path = mod_file.parent / folder_path[4:]
        elif not Path(folder_path).is_absolute():
            folder_path = mod_file.parent / folder_path

        if not Path(folder_path).exists():
            logging.warning("解析得到的模组路径不存在: %s", folder_path)
            return None

        mod_name = mod_file.stem
        match_name = re.search(r'name\s*=\s*"\s*([^"]+?)\s*"', content)
        if match_name:
            mod_name = match_name.group(1).strip()

        mod_version = ""
        match_version = re.search(r'version\s*=\s*"\s*([^"]+?)\s*"', content)
        if match_version:
            mod_version = match_version.group(1).strip()

        remote_id = ""
        match_remote = re.search(r'remote_file_id\s*=\s*"?([0-9]+)"?', content)
        if match_remote:
            remote_id = match_remote.group(1).strip()

        return (mod_name, str(folder_path), mod_version, remote_id)


class LocalModsInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LocalModsInterface")
        self.all_mods = []  # 用于存储所有加载的模组数据
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # 顶栏：显示程序标题与进度环（位于右侧）
        top_bar = QWidget(self)
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(18, 24, 18, 10)
        title_label = QLabel("管理Mod", top_bar)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        top_bar_layout.addWidget(title_label)
        top_bar_layout.addStretch()
        self.progress_ring = IndeterminateProgressRing(top_bar)
        self.progress_ring.setFixedSize(30, 30)
        self.progress_ring.hide()
        top_bar_layout.addWidget(self.progress_ring)
        main_layout.addWidget(top_bar)

        # 模组头部：显示“本地Mod”标签、搜索框和刷新按钮
        mod_header = QWidget(self)
        mod_header_layout = QHBoxLayout(mod_header)
        mod_header_layout.setContentsMargins(24, 10, 18, 10)
        local_mod_label = QLabel("本地Mod", mod_header)
        local_mod_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        mod_header_layout.addWidget(local_mod_label)

        mod_header_layout.addStretch()

        self.search_edit = SearchLineEdit(mod_header)
        self.search_edit.setPlaceholderText("搜索mod名称")
        self.search_edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.search_edit.textChanged.connect(self.filter_mods)
        mod_header_layout.addWidget(self.search_edit)

        mod_header_layout.addStretch()

        btn_refresh = PushButton("刷新Mod列表", mod_header)
        btn_refresh.setFixedSize(115, 30)
        btn_refresh.clicked.connect(self.load_mods)
        mod_header_layout.addWidget(btn_refresh)
        main_layout.addWidget(mod_header)

        # 放置模组卡片的容器
        cards_container = QWidget()
        cards_container.setStyleSheet("background-color: transparent;")
        cards_container.setContentsMargins(18, 6, 18, 0)
        self.cards_grid = QGridLayout(cards_container)
        self.cards_grid.setSpacing(10)
        cards_container.setLayout(self.cards_grid)

        scroll_area = SmoothScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(cards_container)
        scroll_area.setStyleSheet("QScrollArea { background: transparent; }")
        main_layout.addWidget(scroll_area)
        main_layout.setContentsMargins(18, 6, 18, 0)

        self.load_mods()

    def load_mods(self):
        """使用单独线程加载模组卡片，同时显示顶栏进度环"""
        userprofile = os.environ.get("USERPROFILE")
        if not userprofile:
            logging.error("无法获取 USERPROFILE 环境变量")
            return

        mod_dir = Path(userprofile) / "Documents" / "Paradox Interactive" / "Hearts of Iron IV" / "mod"
        if not mod_dir.exists():
            logging.error("Mod路径不存在: %s", mod_dir)
            return

        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 显示顶栏进度环
        self.progress_ring.show()

        self.loader_thread = QThread(self)
        self.mod_loader = ModLoader(mod_dir)
        self.mod_loader.moveToThread(self.loader_thread)
        self.loader_thread.started.connect(self.mod_loader.run)
        self.mod_loader.finished.connect(self.handle_mods_loaded)
        self.mod_loader.finished.connect(self.loader_thread.quit)
        self.mod_loader.finished.connect(self.mod_loader.deleteLater)
        self.loader_thread.finished.connect(self.loader_thread.deleteLater)
        self.loader_thread.start()

    def handle_mods_loaded(self, mods):
        """加载完成后更新数据并隐藏顶栏进度环"""
        self.all_mods = mods
        self.filter_mods()
        self.progress_ring.hide()

    def filter_mods(self):
        """根据搜索框关键字过滤模组并更新显示"""
        query = self.search_edit.text().strip().lower()
        if not self.all_mods:
            return

        filtered_mods = self.all_mods if query == "" else [mod for mod in self.all_mods if query in mod[0].lower()]
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._populate_grid(filtered_mods)

    def _populate_grid(self, mods):
        """根据模组数据填充卡片网格"""
        columns = 2
        row, col = 0, 0
        for mod_name, folder_path, mod_version, remote_id in mods:
            card = CardWidget(self)
            card_layout = QHBoxLayout(card)
            card.setLayout(card_layout)

            thumb_label = QLabel(card)
            thumb_label.setFixedSize(100, 100)
            thumb_path = Path(folder_path) / "thumbnail.png"
            if thumb_path.is_file():
                pixmap = QPixmap(str(thumb_path))
            else:
                default_thumbnail = Path("HOIModEditor/main/resource/images/noneimage.png")
                if default_thumbnail.is_file():
                    pixmap = QPixmap(str(default_thumbnail))
                else:
                    logging.warning("图标不存在：%s", default_thumbnail)
                    pixmap = QPixmap()
            scaled_pixmap = pixmap.scaled(100, 100,
                                          Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            thumb_label.setPixmap(scaled_pixmap)
            card_layout.addWidget(thumb_label)

            text_container = QWidget(card)
            text_layout = QVBoxLayout(text_container)
            text_container.setLayout(text_layout)
            name_label = QLabel(mod_name, card)
            name_label.setWordWrap(True)
            name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
            text_layout.addWidget(name_label)
            if mod_version:
                version_label = QLabel(f"Mod版本：{mod_version}", card)
                version_label.setStyleSheet("font-size: 14px; color: gray;")
                text_layout.addWidget(version_label)
            card_layout.addWidget(text_container)
            card_layout.addStretch()

            icon_path = ("HOIModEditor/main/resource/images/icons/modlist/steam.png"
                         if remote_id else
                         "HOIModEditor/main/resource/images/icons/modlist/local.png")
            icon_label = QLabel(card)
            icon_pixmap = QPixmap(icon_path)
            if not icon_pixmap.isNull():
                scaled_icon = icon_pixmap.scaled(25, 25,
                                                 Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation)
                icon_label.setPixmap(scaled_icon)
            else:
                logging.warning("图标不存在: %s", icon_path)
            text_layout.addWidget(icon_label)

            button_container = QWidget(card)
            btn_layout = QVBoxLayout(button_container)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(5)

            btn_open = PrimaryPushButton("打开Mod文件夹", card)
            btn_open.clicked.connect(lambda checked, path=folder_path: webbrowser.open(Path(path).as_uri()))
            btn_layout.addWidget(btn_open)

            if remote_id:
                btn_steam = PrimaryPushButton("打开Steam页面", card)
                btn_steam.clicked.connect(lambda checked, rid=remote_id: webbrowser.open(
                    f"https://steamcommunity.com/sharedfiles/filedetails/?id={rid}"
                ))
                btn_layout.addWidget(btn_steam)

            card_layout.addWidget(button_container)
            self.cards_grid.addWidget(card, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1