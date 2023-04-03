# 机 构：中国科学院大学
# 程序员：李浩东
# 时 间：2023/4/2 11:33

import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class  Hexadecimal(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.setWindowTitle("十六进制信息")
        # 设置显示二进制信息数据区域
        self.data_area_n = QTextBrowser()
        self.grid_data = QGridLayout()
        self.grid_data.addWidget(self.data_area_n)
        # 设置关闭按钮
        self.buttonLayout = QHBoxLayout()
        self.close = QPushButton("关闭")
        self.buttonLayout.addWidget(self.close)
        self.close.setFixedWidth(100)
        self.close.setFixedHeight(42)
        font = QFont()
        font.setPixelSize(16)
        self.close.setFont(font)
        # 将解析数据区域和按钮加入总体窗口布局
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.grid_data)
        self.layout.addLayout(self.buttonLayout)
        # 按钮点击事件的定义
        self.close.clicked.connect(self.closeClicked)

        # 从gui.py中生成的二进制信息out_bin.txt文件中读入数据
        with open('out_hex.txt', encoding='UTF-8') as file_obj:
            self.data_area_n.append(file_obj.read())
        os.remove('out_hex.txt')  # 删除out_bin.txt文件

    # 按钮点击事件的实现
    def closeClicked(self):
        self.hide()