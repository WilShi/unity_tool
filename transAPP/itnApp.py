from pathlib import Path
import sys
from main import main

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

class ItnApp(QWidget):
    def __init__(self):
        super().__init__()

        # 按钮
        self.selectfileBtn = QPushButton(self)
        self.selectfileBtn.setText("选择文件")
        self.selectfileBtn.setFixedSize(100,40)

        self.startitnBtn = QPushButton(self)
        self.startitnBtn.setText("开始国际化")
        self.startitnBtn.setFixedSize(100,40)

        self.transBtn = QPushButton(self)
        self.transBtn.setText("翻译")
        self.transBtn.setFixedSize(100,40)

        self.outputBtn = QPushButton(self)
        self.outputBtn.setText("导出")
        self.outputBtn.setFixedSize(100,40)

        # 标签
        self.reactfileLable = QLabel(self)
        self.reactfileLable.setText("React文件:")

        self.tagLable = QLabel(self)
        self.tagLable.setText("标签:")

        self.creatorLable = QLabel(self)
        self.creatorLable.setText("操作人:")

        self.singleLable = QLabel(self)
        self.singleLable.setText("单个国际化:")


        # 输入框
        self.tagInline = QLineEdit(self)
        self.tagInline.setFixedSize(100,40)
        self.tagInline.setText("CRM")

        self.creatorInline = QLineEdit(self)
        self.creatorInline.setFixedSize(100,40)
        self.creatorInline.setText("Wilson Shi")

        self.singletextinput = QTextEdit(self)

        # 显示框
        self.outputres = QTextBrowser(self)


        # 布局
        # 中段
        self.vfileSilder = QVBoxLayout()

        self.hreactfile = QHBoxLayout()
        self.hreactfile.addWidget(self.reactfileLable)
        self.hreactfile.addWidget(self.selectfileBtn)
        self.htag = QHBoxLayout()
        self.htag.addWidget(self.tagLable)
        self.htag.addWidget(self.tagInline)
        self.hcreator = QHBoxLayout()
        self.hcreator.addWidget(self.creatorLable)
        self.hcreator.addWidget(self.creatorInline)

        self.vfileSilder.addLayout(self.hreactfile)
        self.vfileSilder.addLayout(self.htag)
        self.vfileSilder.addLayout(self.hcreator)
        self.vfileSilder.setContentsMargins(0,0,250,0)

        self.hfilesilder = QHBoxLayout()
        self.hfilesilder.addLayout(self.vfileSilder)
        self.hfilesilder.addWidget(self.startitnBtn)
        self.hfilesilder.setContentsMargins(0,0,0,20)

        # 下半段
        self.vbuttons = QVBoxLayout()
        self.vbuttons.addWidget(self.transBtn)
        self.vbuttons.addWidget(self.outputBtn)

        self.hsinglepart = QHBoxLayout()
        self.hsinglepart.addWidget(self.singletextinput)
        self.hsinglepart.addLayout(self.vbuttons)
        self.hsinglepart.addWidget(self.outputres)

        self.vdownpart = QVBoxLayout()
        self.vdownpart.addWidget(self.singleLable)
        self.vdownpart.addLayout(self.hsinglepart)

        # 整页
        self.vmainpart = QVBoxLayout()
        self.vmainpart.addLayout(self.hfilesilder)
        self.vmainpart.addLayout(self.vdownpart)

        self.setLayout(self.vmainpart)
        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) # 美化风格
        self.initUI()

        self.filepath = ''

        self.selectfileBtn.clicked.connect(self.selectfile)


    # 初始化界面
    def initUI(self):
        self.resize(600, 400)
        self.center()
        self.setWindowTitle('React国际化')
        # self.setWindowIcon(QIcon('resource/image/favicon.ico'))
        self.show()

    # 窗口显示居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 设置输入的文件路径
    def selectfile(self):
        self.filepath = QFileDialog.getExistingDirectory(self, "选取需要国际化的文件", str(Path.home()))
        outputpath = QFileDialog.getExistingDirectory(self, "选取导出文件的路径", '.')

    # 开始国际化
    def startitn(self):
        if self.filepath == '': self.selectfile()
        pass

    # 翻译单个输入的字段
    def transsiingle(self):
        pass

    # 导出单个翻译的EXCEL格式文件
    def outputexcel(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ItnApp()
    sys.exit(app.exec_())

