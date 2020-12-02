import sys
from PyQt5 import QtWidgets
from add import AddForm
from text import UserForm
from reg import RegForm
from login import LoginForm


class MainForm(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.f = True
        self.ui = LoginForm(self)
        self.change()

    def change(self):
        self.ui.hide()
        if self.f:
            self.ui = LoginForm(self)
        else:
            self.ui = RegForm(self)
        self.f = not self.f
        self.ui.show()

    def ok(self, key):
        self.ui.hide()
        self.ui = UserForm(self, key)
        self.ui.show()

    def add(self, key):
        self.ui2 = AddForm(self, key)
        self.ui2.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainForm()
    sys.exit(app.exec())