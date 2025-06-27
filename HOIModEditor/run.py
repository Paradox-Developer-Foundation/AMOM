# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from HOIModEditor.main.view.main_window import MainWindow

app = QApplication(sys.argv)
app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

Window = MainWindow()
Window.show()

sys.exit(app.exec())