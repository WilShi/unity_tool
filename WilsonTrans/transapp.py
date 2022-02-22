import random
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget,
    QMessageBox, QHBoxLayout, QVBoxLayout, QSlider, QListWidget,
    QPushButton, QLabel, QComboBox, QFileDialog, QLineEdit, QTextEdit, QTextBrowser)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os, time
import configparser
import qdarkstyle

class Transapp(QWidget):
    def __init__(self):
        super().__init__()

        self.DocBtn = QPushButton(self)
        self.DocBtn.setText("文档翻译")
        # self.DocBtn.setFixedSize(60, 28)

        self.tansBtn = QPushButton(self)
        self.tansBtn.setText("翻译")
        # self.tansBtn.setFixedSize(60, 28)


        self.textinput = QTextEdit(self)
        self.outputres = QTextBrowser(self)

        self.vButtonSilder = QVBoxLayout() # 布局按钮
        self.vButtonSilder.addWidget(self.DocBtn)
        self.vButtonSilder.addWidget(self.tansBtn)

        self.hBoxSlider = QHBoxLayout() # 主布局
        self.hBoxSlider.addWidget(self.textinput)
        self.hBoxSlider.addLayout(self.vButtonSilder)
        self.hBoxSlider.addWidget(self.outputres)

        self.setLayout(self.hBoxSlider)
        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) # 美化风格

        self.DocBtn.clicked.connect(self.transDoc)
        self.tansBtn.clicked.connect(self.transText)

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.resize(600, 400)
        self.center()
        self.setWindowTitle('中英翻译器')
        # self.setWindowIcon(QIcon('resource/image/favicon.ico'))
        self.show()

    # 窗口显示居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 翻译文本
    def transText(self):
        pass


    # 翻译文档
    def transDoc(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Transapp()
    sys.exit(app.exec_())