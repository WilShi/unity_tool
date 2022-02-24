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

        self.selectdicBtn = QPushButton(self)
        self.selectdicBtn.setText("选择文件")
        self.selectdicBtn.setFixedSize(100,40)

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
        self.reactfileLable.setText("*React文件:")

        self.tagLable = QLabel(self)
        self.tagLable.setText("*通配符标签:")

        self.creatorLable = QLabel(self)
        self.creatorLable.setText("*操作人:")

        self.dicfileLable = QLabel(self)
        self.dicfileLable.setText("字典文件:")

        self.appcodeLable = QLabel(self)
        self.appcodeLable.setText("*APP Code:")

        self.singleLable = QLabel(self)
        self.singleLable.setText("单个国际化:")


        # 输入框
        self.tagInline = QLineEdit(self)
        self.tagInline.setFixedSize(100,40)
        self.tagInline.setText("CRM")

        self.creatorInline = QLineEdit(self)
        self.creatorInline.setFixedSize(100,40)
        self.creatorInline.setText("Wilson Shi")

        self.appcodeInline = QLineEdit(self)
        self.appcodeInline.setFixedSize(100,40)
        self.appcodeInline.setText("CRM")

        self.singletextinput = QTextEdit(self)

        # 显示框
        self.outputres = QTextBrowser(self)


        # 布局
        # 上半段
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
        self.vfileSilder.setContentsMargins(0,0,20,0)

        self.vtopmiddleSilder = QVBoxLayout()
        self.hdic = QHBoxLayout()
        self.hdic.addWidget(self.dicfileLable)
        self.hdic.addWidget(self.selectdicBtn)
        self.happcode = QHBoxLayout()
        self.happcode.addWidget(self.appcodeLable)
        self.happcode.addWidget(self.appcodeInline)
        self.vtopmiddleSilder.addLayout(self.hdic)
        self.vtopmiddleSilder.addLayout(self.happcode)
        self.vtopmiddleSilder.setContentsMargins(0,0,20,0)

        self.hfilesilder = QHBoxLayout()
        self.hfilesilder.addLayout(self.vfileSilder)
        self.hfilesilder.addLayout(self.vtopmiddleSilder)
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
        self.dicpath = ''
        self.temptrans = []

        self.selectfileBtn.clicked.connect(self.selectfile)
        self.selectdicBtn.clicked.connect(self.selectdicfile)
        self.startitnBtn.clicked.connect(self.startitn)
        self.transBtn.clicked.connect(self.transsingle)
        self.outputBtn.clicked.connect(self.outputexcel)


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
        self.filepath = QFileDialog.getExistingDirectory(self, "选取需要国际化的文件", str(Path.home())+"/Desktop")
        
    # 设置字典路径
    def selectdicfile(self):
        self.filepath = QFileDialog.getExistingDirectory(self, "选取字典文件", str(Path.home())+"/Desktop")

    # 开始国际化
    def startitn(self):
        if self.filepath == '': self.selectfile()
        if self.checkinput():
            outputpath = QFileDialog.getExistingDirectory(self, "选取导出文件的路径", str(Path.home())+"/Downloads")

            react_path = self.filepath
            dic = self.dicpath

            tag = self.tagInline.text()
            appcode = self.appcodeInline.text()
            creator = self.creatorInline.text()

            self.startitnBtn.setText("正在国际化...")
            QApplication.processEvents()
            # time.sleep(5)
            # print(react_path, tag, dic, appcode, creator, outputpath)
            main(react_path, tag, dic=dic, appCode=appcode, creator=creator, outputpath=outputpath).start()

            self.startitnBtn.setText("开始国际化")
            self.Tips(f"国际化已完成!!!\n文件保存在：{outputpath}")
        

    # 翻译单个输入的字段
    def transsingle(self):
        words = self.singletextinput.toPlainText().split('\n')
        if len(words) and not words[0]: return self.outputres.setText('')
        output = []
        for word in words:
            if word:
                res = main(self.filepath, self.tagInline.text(), dic=self.dicpath, appCode=self.appcodeInline.text(), \
                    creator=self.creatorInline.text()).transwords(word)
                self.temptrans.append(res)
                output.append(res['en'])
                output.append(f"$t(\'{res['key']}\')")
                output.append("-"*20)
            else:
                output.append('')
                output.append('')
                output.append("-"*20)
        self.outputres.setText('\n'.join(output))
        QApplication.processEvents()


    # 导出单个翻译的EXCEL格式文件
    def outputexcel(self):
        if self.checkinput():
            outputpath = QFileDialog.getExistingDirectory(self, "选取导出文件的路径", str(Path.home())+"/Downloads")
            if not outputpath: return
            if not self.outputres.toPlainText(): self.transsingle()
            main(self.filepath, self.tagInline.text(), dic=self.dicpath, appCode=self.appcodeInline.text(), \
                creator=self.creatorInline.text(), outputpath=outputpath).outputexcel(self.temptrans)
            self.Tips(f"国际化已完成!!!\n文件保存在：{outputpath}")

    # 检测是否已填所有必填项
    def checkinput(self):
        if self.tagInline.text() and self.creatorInline.text() and self.appcodeInline.text():
            return True
        else:
            self.Tips("缺少必填项！！！")
            return False

    # 提示
    def Tips(self, message):
        QMessageBox.about(self, "提示", message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ItnApp()
    sys.exit(app.exec_())

