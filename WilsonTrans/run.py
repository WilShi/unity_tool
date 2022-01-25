import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_tranView import Ui_Form
from trans import lang

class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None) -> None:
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.display)


    def display(self):
        words = self.lineEdit.text()

        output = lang().translate(words)

        self.text_output_Browser.setText(output)
        QApplication.processEvents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
