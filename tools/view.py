import os
import sys
import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from qfluentwidgets import CardWidget, PrimaryPushButton
def iter_mod_folders():
    user_profile = os.environ.get("USERPROFILE")
    if not user_profile:
        return
    base_dir = os.path.join(user_profile, "Documents", "Paradox Interactive", "Hearts of Iron IV", "mod")
    if not os.path.exists(base_dir):
        return
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path) and os.path.exists(os.path.join(folder_path, "descriptor.mod")):
            yield (folder, folder_path)
def get_mod_name(folder_path: str) -> str:
    descriptor_path = os.path.join(folder_path, "descriptor.mod")
    try:
        with open(descriptor_path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.search(r'name\s*=\s*"(.+?)"', line.strip())
                if m:
                    return m.group(1)
    except Exception as e:
        print(f"Error reading mod name from {descriptor_path}: {e}")
    return ""
def open_folder(folder_path: str):
    try:
        os.startfile(folder_path)
    except Exception as e:
        print(f"无法打开文件夹 {folder_path}: {e}")
class ModCardWidget(CardWidget):
    def __init__(self, folder_name: str, folder_path: str, parent=None):
        super().__init__(parent)
        mod_title = get_mod_name(folder_path)
        if not mod_title:
            mod_title = folder_name
        outer_layout = QHBoxLayout(self)
        outer_layout.setContentsMargins(10, 10, 10, 10)
        outer_layout.setSpacing(10)
        image_label = QLabel(self)
        thumbnail_path = os.path.join(folder_path, "thumbnail.png")
        if os.path.exists(thumbnail_path):
            pixmap = QPixmap(thumbnail_path)
            pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("无图像")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setFixedSize(100, 100)
        outer_layout.addWidget(image_label)
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(0, 0, 0, 0)
        title_label = QLabel(mod_title, self)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        right_layout.addWidget(title_label)
        detail_label = QLabel("包含 descriptor.mod 文件", self)
        right_layout.addWidget(detail_label)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        open_btn = PrimaryPushButton("打开文件夹", self)
        open_btn.clicked.connect(lambda _, path=folder_path: open_folder(path))
        btn_layout.addWidget(open_btn)
        right_layout.addLayout(btn_layout)
        outer_layout.addLayout(right_layout)
        self.setLayout(outer_layout)
def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("本地Mod列表")
    window.resize(1280, 720)
    main_h_layout = QHBoxLayout(window)
    main_h_layout.setContentsMargins(10, 10, 10, 10)
    main_h_layout.setSpacing(5)
    viewport = QFrame(window)
    viewport.setFrameShape(QFrame.Shape.NoFrame)
    viewport.setStyleSheet("background: transparent;")
    viewport.setFixedWidth(1280)
    container_widget = QWidget(viewport)
    container_h_layout = QHBoxLayout(container_widget)
    container_h_layout.setContentsMargins(0, 0, 0, 0)
    container_h_layout.setSpacing(15)
    left_column = QWidget(container_widget)
    left_layout = QVBoxLayout(left_column)
    left_layout.setContentsMargins(10, 10, 10, 10)
    left_layout.setSpacing(15)
    left_column.setLayout(left_layout)
    right_column = QWidget(container_widget)
    right_layout = QVBoxLayout(right_column)
    right_layout.setContentsMargins(10, 10, 10, 10)
    right_layout.setSpacing(15)
    right_column.setLayout(right_layout)
    container_h_layout.addWidget(left_column)
    container_h_layout.addWidget(right_column)
    container_widget.setLayout(container_h_layout)
    toggle = True
    found = False
    for folder_name, folder_path in iter_mod_folders():
        found = True
        mod_card = ModCardWidget(folder_name, folder_path, container_widget)
        if toggle:
            left_layout.addWidget(mod_card)
        else:
            right_layout.addWidget(mod_card)
        toggle = not toggle
    if not found:
        msg = QLabel("未找到Mod", container_widget)
        container_h_layout.addWidget(msg)
    container_widget.adjustSize()
    viewport_layout = QVBoxLayout(viewport)
    viewport_layout.setContentsMargins(0, 0, 0, 0)
    viewport_layout.addWidget(container_widget)
    viewport.setLayout(viewport_layout)
    scroll_bar = QScrollBar(Qt.Orientation.Vertical, window)
    def on_scroll(value):
        container_widget.move(0, -value)
    scroll_bar.valueChanged.connect(on_scroll)
    main_h_layout.addWidget(viewport)
    main_h_layout.addWidget(scroll_bar)
    window.setLayout(main_h_layout)
    window.show()
    def update_scroll_range():
        content_height = container_widget.sizeHint().height()
        viewport_height = viewport.height()
        scroll_bar.setRange(0, max(0, content_height - viewport_height))
    update_scroll_range()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()