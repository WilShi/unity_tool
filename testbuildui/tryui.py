import sys
from PyQt5.QtWidgets import QApplication, QStackedLayout, QWidget

# 制作堆叠布局的教程：https://blog.csdn.net/qq_39177678/article/details/108166480

# 导入生成的 ui
from main_ui import Ui_blog_page
from home_page import Ui_home_page
from blog_page import Ui_main
from MP3Player import MP3Player


class FrameHomePage(QWidget, Ui_home_page):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class FrameBlogPage(QWidget, Ui_blog_page):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class FrameContactPage(QWidget, MP3Player):
    def __init__(self):
        super().__init__()
        self.initUI()


class MainWidget(QWidget, Ui_main):
    """
    主窗口
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 实例化一个堆叠布局
        self.qsl = QStackedLayout(self.frame)
        # 实例化分页面
        self.home = FrameHomePage()
        self.blog = FrameBlogPage()
        self.contact = FrameContactPage()
        # 加入到布局中
        self.qsl.addWidget(self.home)
        self.qsl.addWidget(self.blog)
        self.qsl.addWidget(self.contact)
        # 控制函数
        self.controller()

    def controller(self):
        self.pushButton.clicked.connect(self.switch)
        self.pushButton_2.clicked.connect(self.switch)
        self.pushButton_3.clicked.connect(self.switch)

    def switch(self):
        sender = self.sender().objectName()

        index = {
            "pushButton": 0,
            "pushButton_2": 1,
            "pushButton_3": 2,
        }

        self.qsl.setCurrentIndex(index[sender])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MainWidget()
    myWin.show()
    sys.exit(app.exec_())