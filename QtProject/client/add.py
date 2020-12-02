from PyQt5 import QtWidgets, QtCore, QtGui
# В данном файле находится окно для добавления данных в таблицу
import socket
import shlex
q = shlex.quote


class AddForm(QtWidgets.QDialog):
    def __init__(self, par, id):
        super().__init__()
        self.file = None
        self.par = par
        self.key = id
        self.setupUi()

    def setupUi(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("image/add_im.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.setObjectName("self")
        self.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(self)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.name_input = QtWidgets.QLineEdit(self)
        self.name_input.setObjectName("name_input")
        self.gridLayout.addWidget(self.name_input, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.ok_btn = QtWidgets.QPushButton(self)
        self.ok_btn.setObjectName("pushButton")
        self.gridLayout.addWidget(self.ok_btn, 3, 0, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
        self.plainTextEdit.setObjectName("ok_btn")
        self.gridLayout.addWidget(self.plainTextEdit, 1, 1, 1, 1)
        self.add_btn = QtWidgets.QPushButton(self)
        self.add_btn.setObjectName("add_btn")
        self.gridLayout.addWidget(self.add_btn, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.fname_out = QtWidgets.QLabel(self)
        self.fname_out.setText("")
        self.fname_out.setObjectName("fname_out")
        self.gridLayout.addWidget(self.fname_out, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.retranslateUi()
        self.add_btn.clicked.connect(self.add)
        self.ok_btn.clicked.connect(self.ok)
        QtCore.QMetaObject.connectSlotsByName(self)

    def add(self):
        # Функция для прикрепления данных
        self.file, ok = QtWidgets.QFileDialog().getOpenFileName()
        self.fname_out.setText(self.file)

    def ok(self):
        # Функция для отправки данных на сервер
        name = self.name_input.text().replace('"', '').replace("'", '')
        about = self.plainTextEdit.toPlainText().replace('"', '').replace("'", '')
        file_name = self.file
        if file_name:
            file_name = file_name.split('/')[-1].replace('"', '').replace("'", '')
        sock = socket.socket()
        sock.connect(('localhost', 20951))
        sock.settimeout(1)
        try:
            sock.send(f"add_row {q(self.key.decode('utf-8'))} {q(name)} {q(about)}"
                      f" {q(file_name if file_name else '#None#')} ".encode('utf-8').ljust(1024, b'0'))
        except Exception as e:
            print(e, '\nLINE 69')
        try:
            if file_name:
                with open(self.file, 'rb') as file:
                    data = file.read(1024)
                    while data:
                        sock.send(data)
                        data = file.read(1024)
                    file.close()
        except Exception as e:
            print(e, '\nLINE 81')
        sock.send(b'')
        sock.close()
        self.par.ui.loadTable()
        self.hide()

    def retranslateUi(self):
        self.setWindowTitle('Добавить')
        self.label.setText("Название")
        self.ok_btn.setText("Добавить")
        self.add_btn.setText("Прикрепить файл")
        self.label_2.setText("Описание")