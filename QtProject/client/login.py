# -*- coding: utf-8 -*-
# В данном файле хранится форма для входа
from PyQt5 import QtCore, QtGui, QtWidgets
import hashlib
import socket
import shlex
q = shlex.quote


def sleep(seconds):
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(seconds * 1000, loop.quit)
    loop.exec_()


class LoginForm(QtWidgets.QDialog):
    def __init__(self, par):
        super().__init__()
        self.par = par
        self.setupUi()
        self.retranslateUi()

    def print_err(self, text):
        # Функция выведения сообщения в StatusBar
        self.err_out.resize(self.size().width(), 30)
        self.err_out.show()
        self.err_out.showMessage(text)
        sleep(2)
        self.err_out.hide()

    def setupUi(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("image/login_im.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.setObjectName("self")
        self.resize(569, 574)
        self.err_out = QtWidgets.QStatusBar(self)
        self.err_out.setStyleSheet('background-color: red;')
        self.err_out.hide()
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.ok_btn = QtWidgets.QPushButton(self)
        self.ok_btn.setStyleSheet("background-color: rgb(255, 0, 4);\n"
"font: 75 12pt \"MS Shell Dlg 2\";\n"
"border-radius: 7px;\n"
"width: 80px;")
        self.ok_btn.setObjectName("ok_btn")
        self.gridLayout_2.addWidget(self.ok_btn, 3, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 3, 2, 1, 1)
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setObjectName("password_input")
        self.gridLayout_2.addWidget(self.password_input, 2, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.new_action = QtWidgets.QLabel(self)
        self.new_action.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 255);")
        self.new_action.setObjectName("new_action")
        self.gridLayout_2.addWidget(self.new_action, 4, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 3, 0, 1, 1)
        self.login_input = QtWidgets.QLineEdit(self)
        self.login_input.setObjectName("login_input")
        self.gridLayout_2.addWidget(self.login_input, 1, 1, 1, 2)
        self.label = QtWidgets.QLabel(self)
        self.label.setMaximumHeight(120)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 3)
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 4, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.new_action.mousePressEvent = self.new
        self.ok_btn.clicked.connect(self.on_click)

    def new(self, event):
        # Запуск формы регистрации
        self.par.change()

    def on_click(self):
        # Процесс регистрации распололжен ниже
        login = self.login_input.text().lower()
        try:
            sock = socket.socket()
            sock.connect(('localhost', 20951))
            sock.settimeout(1)
            sock.send(f'login_get_salt {login}'.encode('utf-8'))
            salt = sock.recv(1024)
            print(salt)
            sock.close()

        except Exception:
            self.print_err('Связка данного имени пользователя и пароля не найдена.')
            return

        password = self.password_input.text()
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        try:
            sock = socket.socket()
            sock.connect(('localhost', 20951))
            sock.settimeout(1)
            sock.send(f'login {login} '.encode('utf-8') + q(str(key)[2:-1]).encode('utf-8'))
            self.id = sock.recv(1024)
            sock.close()
        except Exception:
            self.print_err('Связка данного имени пользователя и пароля не найдена.')
            return
        self.err_out.setStyleSheet('background-color: green')
        self.print_err('Успешный вход!')
        self.err_out.setStyleSheet('background-color: red')
        try:
            self.par.ok(self.id)
        except Exception as e:
            print(e, "\nLINE 134")


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Вход"))
        self.label_3.setText(_translate("self", "Пароль:"))
        self.ok_btn.setText(_translate("self", "Войти"))
        self.label_2.setText(_translate("self", "Логин:"))
        self.new_action.setText(_translate("self", "Зарегистрироваться"))
        self.label.setText(_translate("self", "Вход"))
        self.label_4.setText(_translate("self", "Еще не зарегистрирован?"))