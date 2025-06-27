import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QCheckBox, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from qfluentwidgets import CardWidget, PushButton, LineEdit, TitleLabel


class CreateModInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.option_checkboxes = []
        self.initUI()

    def initUI(self):
        self.setObjectName("CreateModInterface")
        self.setWindowTitle("创建 Mod")
        self.resize(600, 500)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 上部容器：包括顶部标题和输入区域
        upper_container = QWidget(self)
        upper_layout = QVBoxLayout(upper_container)
        upper_layout.setContentsMargins(18, 6, 18, 0)
        upper_layout.setSpacing(10)

        # 顶部标题栏
        top_bar = QWidget(upper_container)
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(10, 10, 10, 10)
        self.add_title_label(top_bar_layout, "创建Mod")
        upper_layout.addWidget(top_bar)

        # 卡片容器（输入项和标签选择）
        cards_container = QWidget(upper_container)
        cards_layout = QGridLayout(cards_container)
        cards_layout.setSpacing(10)

        # 使用辅助函数创建输入项卡片
        self.mod_name_card, self.mod_name_input = self.create_input_card(
            "请输入 Mod 名称", "Mod 名称", cards_container
        )
        self.mod_version_card, self.mod_version_input = self.create_input_card(
            "请输入 Mod版本", "Mod版本", cards_container
        )
        self.mod_folder_card, self.mod_folder_input = self.create_input_card(
            "请输入Mod文件夹名称", "Mod文件夹名称", cards_container
        )
        self.supported_version_card, self.supported_game_version_input = self.create_input_card(
            "请输入支持的游戏版本", "支持的游戏版本", cards_container
        )

        cards_layout.addWidget(self.mod_name_card, 0, 0)
        cards_layout.addWidget(self.mod_version_card, 0, 1)
        cards_layout.addWidget(self.mod_folder_card, 1, 0)
        cards_layout.addWidget(self.supported_version_card, 1, 1)

        # 标签选项卡片
        options_card = CardWidget(cards_container)
        options_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        options_layout = QVBoxLayout(options_card)
        title_label_options = TitleLabel("请选择标签（最多选择10项）", options_card)
        title_label_options.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_font = title_label_options.font()
        title_font.setPointSize(14)
        title_label_options.setFont(title_font)
        options_layout.addWidget(title_label_options)

        checkboxes_layout = QGridLayout()
        checkboxes_layout.setSpacing(10)
        options_list = [
            "Alternative History",
            "Balance",
            "Events",
            "Fixes",
            "Gameplay",
            "Graphics",
            "Historical",
            "Map",
            "Ideologies",
            "Military",
            "National Focuses",
            "Sound",
            "Technologies",
            "Translation",
            "Utilities"
        ]
        # 对应每个选项的注释
        annotations = [
            " - 架空历史",
            " - 平衡性",
            " - 事件",
            " - 修复",
            " - 玩法模式",
            " - 图像",
            " - 历史性",
            " - 地图",
            " - 意识形态",
            " - 军事",
            " - 国策",
            " - 音效音乐",
            " - 科技",
            " - 翻译",
            " - 实用"
        ]
        for index, option in enumerate(options_list):
            # 创建一个容器放置复选框和注释，设置尺寸策略为Minimum，确保只占用必要宽度
            container = QWidget(options_card)
            container.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            hbox_layout = QHBoxLayout(container)
            hbox_layout.setContentsMargins(0, 0, 0, 0)
            hbox_layout.setSpacing(0)  # 无间距，确保文本紧跟

            # 创建复选框，自动调整宽度
            checkbox = QCheckBox(option, container)
            font_checkbox = checkbox.font()
            font_checkbox.setPointSize(10)
            checkbox.setFont(font_checkbox)
            checkbox.stateChanged.connect(self.update_checkboxes_state)
            checkbox.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            # 根据文本长度计算最小宽度，并添加少量边距
            fm = checkbox.fontMetrics()
            text_min_width = fm.horizontalAdvance(option) + 5
            checkbox.setMinimumWidth(text_min_width)
            self.option_checkboxes.append(checkbox)
            hbox_layout.addWidget(checkbox)

            # 创建注释标签
            annotation_label = QLabel(annotations[index], container)
            font_annotation = annotation_label.font()
            font_annotation.setPointSize(8)
            annotation_label.setFont(font_annotation)
            annotation_label.setStyleSheet("color: gray;")
            annotation_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            hbox_layout.addWidget(annotation_label)

            container.setLayout(hbox_layout)
            checkboxes_layout.addWidget(container, index // 3, index % 3)

        options_layout.addLayout(checkboxes_layout)
        options_card.setLayout(options_layout)
        cards_layout.addWidget(options_card, 2, 0, 1, 2)

        cards_container.setLayout(cards_layout)
        upper_layout.addWidget(cards_container)
        main_layout.addWidget(upper_container)

        # 底部按钮区域
        button_container = QWidget(self)
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        create_button = PushButton("开始创建", self)
        create_button.clicked.connect(self.on_create_clicked)
        button_layout.addWidget(create_button)
        button_container.setLayout(button_layout)
        main_layout.addWidget(button_container)

        main_layout.setStretch(0, 65)
        main_layout.setStretch(1, 35)

        self.setLayout(main_layout)

    def add_title_label(self, layout, text):
        """辅助方法：在指定布局中添加一个标题标签"""
        title_label = QLabel(text)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

    def create_input_card(self, title, placeholder, parent):
        """
        辅助方法：创建一个包含标题和输入框的卡片控件

        参数：
            title: 显示的标题文本
            placeholder: 输入框的占位符文本
            parent: 父控件
        返回：
            卡片控件和对应的 LineEdit 控件
        """
        card = CardWidget(parent)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(card)
        title_label = TitleLabel(title, card)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        font_label = title_label.font()
        font_label.setPointSize(14)
        title_label.setFont(font_label)
        layout.addWidget(title_label)
        input_field = LineEdit(card)
        input_field.setPlaceholderText(placeholder)
        layout.addWidget(input_field)
        card.setLayout(layout)
        return card, input_field

    def update_checkboxes_state(self):
        """当复选框状态变化时更新每个复选框的可用状态，最多只能选10项"""
        selected_count = sum(1 for cb in self.option_checkboxes if cb.isChecked())
        for cb in self.option_checkboxes:
            cb.setDisabled(not cb.isChecked() and selected_count >= 10)

    def on_create_clicked(self):
        """按钮点击事件：生成 mod 的描述文件并写入文件系统"""
        mod_name = self.mod_name_input.text().strip()
        mod_version = self.mod_version_input.text().strip()
        mod_folder = self.mod_folder_input.text().strip()
        supported_game_version = self.supported_game_version_input.text().strip()
        selected_options = [cb.text() for cb in self.option_checkboxes if cb.isChecked()]

        if mod_name and mod_version and mod_folder and supported_game_version:
            content_lines = [
                f'version = "{mod_version}"',
                "tags = {",
                *[f'\t"{opt}"' for opt in selected_options],
                "}",
                f'name = "{mod_name}"',
                f'supported_version = "{supported_game_version}"',
                'picture = "thumbnail.png"'
            ]
            descriptor_content = "\n".join(content_lines)

            user_documents = os.path.join(
                os.environ["USERPROFILE"],
                "Documents",
                "Paradox Interactive",
                "Hearts of Iron IV",
                "mod"
            )
            new_mod_folder = os.path.join(user_documents, mod_folder)
            try:
                os.makedirs(new_mod_folder, exist_ok=True)
                descriptor_file = os.path.join(new_mod_folder, "descriptor.mod")
                with open(descriptor_file, "w", encoding="utf-8") as f:
                    f.write(descriptor_content)

                mod_file_path = os.path.join(user_documents, f"{mod_folder}.mod")
                mod_content = descriptor_content + f'\npath = "mod/{mod_folder}"'
                with open(mod_file_path, "w", encoding="utf-8") as f:
                    f.write(mod_content)

                print("Mod 创建成功")
            except Exception as e:
                print("创建Mod时出错：", e)
        else:
            print("请填写所有必填字段")
