# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\cn-wilsonshi\Desktop\work\unity_tool\main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_blog_page(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(612, 488)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(150, 120, 104, 87))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(290, 230, 104, 87))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.plainTextEdit.setPlainText(_translate("Form", "这里是第二页"))
        self.plainTextEdit_2.setPlainText(_translate("Form", "这里是第二页"))