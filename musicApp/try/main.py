#! -*- coding: utf-8 -*-
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import random
from PyQt5.QtWidgets import (QWidget, QDesktopWidget,
    QMessageBox, QHBoxLayout, QVBoxLayout, QSlider, QListWidget,
    QPushButton, QLabel, QComboBox, QFileDialog)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QUrl, QTimer, QCoreApplication 
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os, time
import configparser
import qdarkstyle

from Ui_main import Ui_From


class MyMainForm(QMainWindow, Ui_From):
    def __init__(self, parent=None) -> None:

        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) # 美化风格

        self.song_formats = ['mp3', 'm4a', 'flac', 'wav', 'ogg']
        self.songs_list = []
        self.cur_playing_song = ''
        self.is_pause = True
        self.player = QMediaPlayer()
        self.is_switching = False
        self.playMode = 0
        self.settingfilename = 'config.ini'

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.playByMode)

        self.play_pushButton.setStyleSheet("QPushButton{border-image: url(resource/image/play.png)}")
        self.play_pushButton.setText('')
        self.play_pushButton.setFixedSize(30, 30)

        self.next_pushButton.setStyleSheet("QPushButton{border-image: url(resource/image/next.png)}")
        self.next_pushButton.setText('')
        self.next_pushButton.setFixedSize(30, 30)

        self.prev_pushButton.setStyleSheet("QPushButton{border-image: url(resource/image/prev.png)}")
        self.prev_pushButton.setText('')
        self.prev_pushButton.setFixedSize(30, 30)

        self.local_pushButton.setStyleSheet("QPushButton{border-image: url(resource/image/open.png)}")
        self.local_pushButton.setText('')
        self.local_pushButton.setFixedSize(24, 24)

        self.playmode_pushButton.setStyleSheet("QPushButton{border-image: url(resource/image/sequential.png)}")
        self.playmode_pushButton.setText('')
        self.playmode_pushButton.setFixedSize(24, 24)

        
        self.local_pushButton.clicked.connect(self.openMusicFloder)
        self.play_pushButton.clicked.connect(self.playMusic)
        self.prev_pushButton.clicked.connect(self.prevMusic)
        self.next_pushButton.clicked.connect(self.nextMusic)
        self.listWidget.itemDoubleClicked.connect(self.doubleClicked)
        self.horizontalSlider.sliderMoved[int].connect(lambda: self.player.setPosition(self.horizontalSlider.value()))
        self.playmode_pushButton.clicked.connect(self.playModeSet)


        self.loadingSetting()

        
    # 初始化界面
    def initUI(self):
        self.resize(600, 400)
        self.center()
        self.setWindowTitle('音乐播放器')   
        self.setWindowIcon(QIcon('resource/image/favicon.ico'))
        self.show()
        
    # 窗口显示居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 打开文件夹
    def openMusicFloder(self):
        self.cur_path = QFileDialog.getExistingDirectory(self, "选取音乐文件夹", './')
        if self.cur_path:
            self.showMusicList()
            self.cur_playing_song = ''
            self.timestart_label.setText('00:00')
            self.timeend_label.setText('00:00')
            self.horizontalSlider.setSliderPosition(0)
            self.updateSetting()
            self.is_pause = True
            self.play_pushButton.setStyleSheet("QPushButton{border-image: url(resource/image/play.png)}")
    
    # 显示音乐列表
    def showMusicList(self):
        self.listWidget.clear()
        for song in os.listdir(self.cur_path):
            if song.split('.')[-1] in self.song_formats:
                self.songs_list.append([song, os.path.join(self.cur_path, song).replace('\\', '/')])
                self.listWidget.addItem(song)
        self.listWidget.setCurrentRow(0)
        if self.songs_list:
                self.cur_playing_song = self.songs_list[self.listWidget.currentRow()][-1]

    # 提示
    def Tips(self, message):
        QMessageBox.about(self, "提示", message)

    # 设置当前播放的音乐
    def setCurPlaying(self):
        self.cur_playing_song = self.songs_list[self.listWidget.currentRow()][-1]
        self.player.setMedia(QMediaContent(QUrl(self.cur_playing_song)))

    # 播放/暂停播放
    def playMusic(self):
        if self.listWidget.count() == 0:
                self.Tips('当前路径内无可播放的音乐文件')
                return
        if not self.player.isAudioAvailable():
                self.setCurPlaying()
        if self.is_pause or self.is_switching:
                self.player.play()
                self.is_pause = False
                self.play_pushButton.setStyleSheet("QPushButton{border-image: url(resource/image/pause.png)}")
        elif (not self.is_pause) and (not self.is_switching):
                self.player.pause()
                self.is_pause = True
                self.play_pushButton.setStyleSheet("QPushButton{border-image: url(resource/image/play.png)}")
 	
    # 上一曲
    def prevMusic(self):
        self.horizontalSlider.setValue(0)
        if self.listWidget.count() == 0:
            self.Tips('当前路径内无可播放的音乐文件')
            return
        pre_row = self.listWidget.currentRow()-1 if self.listWidget.currentRow() != 0 else self.listWidget.count() - 1
        self.listWidget.setCurrentRow(pre_row)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False

    # 下一曲
    def nextMusic(self):
        self.horizontalSlider.setValue(0)
        if self.listWidget.count() == 0:
            self.Tips('当前路径内无可播放的音乐文件')
            return
        next_row = self.listWidget.currentRow()+1 if self.listWidget.currentRow() != self.listWidget.count()-1 else 0
        self.listWidget.setCurrentRow(next_row)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False  

    # 双击歌曲名称播放音乐
    def doubleClicked(self):
        self.horizontalSlider.setValue(0)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False

    # 根据播放模式自动播放，并刷新进度条
    def playByMode(self):
        # 刷新进度条
        if (not self.is_pause) and (not self.is_switching):
            self.horizontalSlider.setMinimum(0)
            self.horizontalSlider.setMaximum(self.player.duration())
            self.horizontalSlider.setValue(self.horizontalSlider.value() + 1000)
        self.timestart_label.setText(time.strftime('%M:%S', time.localtime(self.player.position()/1000)))
        self.timeend_label.setText(time.strftime('%M:%S', time.localtime(self.player.duration()/1000)))
        # 顺序播放
        if (self.playMode == 0) and (not self.is_pause) and (not self.is_switching):
            if self.listWidget.count() == 0:
                return
            if self.player.position() == self.player.duration():
                self.nextMusic()
        # 单曲循环
        elif (self.playMode == 1) and (not self.is_pause) and (not self.is_switching):
            if self.listWidget.count() == 0:
                return
            if self.player.position() == self.player.duration():
                self.is_switching = True
                self.setCurPlaying()
                self.horizontalSlider.setValue(0)
                self.playMusic()
                self.is_switching = False
        # 随机播放
        elif (self.playMode == 2) and (not self.is_pause) and (not self.is_switching):
            if self.listWidget.count() == 0:
                return
            if self.player.position() == self.player.duration():
                self.is_switching = True
                self.listWidget.setCurrentRow(random.randint(0, self.listWidget.count()-1))
                self.setCurPlaying()
                self.horizontalSlider.setValue(0)
                self.playMusic()
                self.is_switching = False

    # 更新配置文件
    def updateSetting(self):
        config = configparser.ConfigParser()
        config.read(self.settingfilename)
        if not os.path.isfile(self.settingfilename):
            config.add_section('MP3Player')
        config.set('MP3Player', 'PATH', self.cur_path)
        config.write(open(self.settingfilename, 'w'))

    # 加载配置文件
    def loadingSetting(self):
        config = configparser.ConfigParser()
        config.read(self.settingfilename)
        if not os.path.isfile(self.settingfilename):
            return
        self.cur_path = config.get('MP3Player', 'PATH')
        self.showMusicList()
    
    # 播放模式设置
    def playModeSet(self):
        # 设置为单曲循环模式
        if self.playMode == 0:
            self.playMode = 1
            self.playmode_pushButton.setStyleSheet("QPushButton{border-image: url(resource/image/circulation.png)}")
        # 设置为随机播放模式
        elif self.playMode == 1:
            self.playMode = 2
            self.playmode_pushButton.setStyleSheet("QPushButton{border-image: url(resource/image/random.png)}")
        # 设置为顺序播放模式
        elif self.playMode == 2:
            self.playMode = 0
            self.playmode_pushButton.setStyleSheet("QPushButton{border-image: url(resource/image/sequential.png)}")

    # 确认用户是否要真正退出
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "确定要退出吗？", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



if __name__ == "__main__":
    # QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())