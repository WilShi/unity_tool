import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget,
    QMessageBox, QHBoxLayout, QVBoxLayout, QSlider, QListWidget,
    QPushButton, QLabel, QComboBox, QFileDialog, QLineEdit, QTextEdit, 
    QTextBrowser, QInputDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os, time
import configparser
import qdarkstyle
from pathlib import Path
from multiprocessing import Process

from human_face_recognition.find_face import Findface
from human_face_recognition.markvideo import MarkVideo

class Findfaceapp(QWidget):
    def __init__(self):
        super().__init__()

        self.buttonwidth = 120
        self.buttonhight = 120

        # 定义按钮
        self.faceimagewashBtn = QPushButton(self)
        self.faceimagewashBtn.setFixedSize(self.buttonwidth, self.buttonhight)
        self.faceimagewashBtn.setText("人脸图片清洗")

        self.faceimagemarkBtn = QPushButton(self)
        self.faceimagemarkBtn.setFixedSize(self.buttonwidth, self.buttonhight)
        self.faceimagemarkBtn.setText("图片人脸标注")

        self.facevideomarkBtn = QPushButton(self)
        self.facevideomarkBtn.setFixedSize(self.buttonwidth, self.buttonhight)
        self.facevideomarkBtn.setText("视频人脸标注")

        self.faceimageshowmarkBtn = QPushButton(self)
        self.faceimageshowmarkBtn.setFixedSize(self.buttonwidth, self.buttonhight)
        self.faceimageshowmarkBtn.setText("人脸标注展示")

        self.frolimagewashBtn = QPushButton(self)
        self.frolimagewashBtn.setFixedSize(self.buttonwidth, self.buttonhight)
        self.frolimagewashBtn.setText("反光图片清洗")

        self.webcammarkBtn = QPushButton(self)
        self.webcammarkBtn.setFixedSize(self.buttonwidth, self.buttonhight)
        self.webcammarkBtn.setText("摄像头人脸检测")

        self.deletefileBtn = QPushButton(self)
        self.deletefileBtn.setFixedSize(self.buttonwidth, self.buttonhight)
        self.deletefileBtn.setText("删除文件")

        self.pendingBtn = QPushButton(self) # 待开发
        self.pendingBtn.setFixedSize(self.buttonwidth, self.buttonhight)
        self.pendingBtn.setText("待开发")


        self.htoppart = QHBoxLayout()
        self.htoppart.addWidget(self.faceimagewashBtn)
        self.htoppart.addWidget(self.faceimagemarkBtn)
        self.htoppart.addWidget(self.facevideomarkBtn)
        self.htoppart.addWidget(self.faceimageshowmarkBtn)

        self.hdownpart = QHBoxLayout()
        self.hdownpart.addWidget(self.frolimagewashBtn)
        self.hdownpart.addWidget(self.webcammarkBtn)
        self.hdownpart.addWidget(self.deletefileBtn)
        self.hdownpart.addWidget(self.pendingBtn)

        self.vmainpart = QVBoxLayout()
        self.vmainpart.addLayout(self.htoppart)
        self.vmainpart.addLayout(self.hdownpart)

        self.setLayout(self.vmainpart)
        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) # 美化风格
        self.initUI()


        self.faceimagewashBtn.clicked.connect(self.findface)
        self.faceimagemarkBtn.clicked.connect(self.imagefacemark)
        self.facevideomarkBtn.clicked.connect(self.videofacemark)
        # self.faceimageshowmarkBtn.clicked.connect(self.transDoc)
        # self.frolimagewashBtn.clicked.connect(self.transDoc)
        # self.webcammarkBtn.clicked.connect(self.transDoc)
        # self.deletefileBtn.clicked.connect(self.transDoc)

        self.path = ""


    # 初始化界面
    def initUI(self):
        self.resize(600, 400)
        self.center()
        self.setWindowTitle('人脸识别')
        # self.setWindowIcon(QIcon('resource/image/favicon.ico'))
        self.show()

    # 窗口显示居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 人脸图片清洗
    def findface(self):
        path = QFileDialog.getExistingDirectory(self, "选取文件路径", str(Path.home())+"/Downloads")
        if path:
            Process(target=Findface().face, args=(path,)).start()
            self.Tips("已开启后台进程运行......\n最终结果将保存在下载文件夹中")

    # 图片人脸标注
    def imagefacemark(self):
        path = QFileDialog.getExistingDirectory(self, "选取文件路径", str(Path.home())+"/Downloads")
        if path:
            Process(target=Findface().multprocess, args=(path,)).start()
            self.Tips("已开启后台进程运行......\n最终结果将保存在下载文件夹中")

    # 视频人脸标注
    def videofacemark(self):
        self.path = QFileDialog.getOpenFileName(self, "选取视频文件路径", str(Path.home())+"/Downloads")[0] \
            if not self.path else self.path

        if '.mp4' not in self.path and '.avi' not in self.path:
            self.Tips("输入的视频格式错误\n请重新选择(仅支持mp4和avi格式)")
            self.path = ""
            self.videofacemark()
        
        text, ok = QInputDialog.getText(self, '视频格式', '帧率, 宽度, 高度')
        if ok:
            try:
                info = text.split(',') if ',' in text else text.split(' ')
                rate = int(info[0])
                width = int(info[1])
                hight = int(info[2])
                outpath = QFileDialog.getExistingDirectory(self, "选取导出路径", str(Path.home())+"/Downloads")
                name, ok = QInputDialog.getText(self, '名称', '导出视频名称')
                if ok:
                    outpath += f"/{name}" if name else "/output"
                    Process(target=MarkVideo(rate, width, hight).multprocess, args=(self.path,outpath,)).start()
                    self.Tips("已开启后台进程运行......\n最终结果将保存在下载文件夹中")
                    return
                return
            except Exception as error:
                self.Tips("输入的视频格式有误!\n请重新输入")
                self.videofacemark()


    # 提示
    def Tips(self, message):
        QMessageBox.about(self, "提示", message)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Findfaceapp()
    sys.exit(app.exec_())