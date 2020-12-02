# -*- coding: utf-8 -*-
# Самая сложная часть проекта - серверная
import sqlite3
import uuid
import socket
import shlex
import os
import datetime
con = sqlite3.connect(r'info.db')
cur = con.cursor()
qte = shlex.quote


def reg_check_login(login):
    # Проверка логина на существование
    return len(list(cur.execute(rf'SELECT name FROM login WHERE name = ?', (login, )))) > 0


def reg(login, salt, key):
    # Функция сохранения аккаунта в базу данных
    if reg_check_login(login):
        return
    cur.execute(fr'INSERT INTO login (name, salt, key) VALUES (?, ?, ?)', (login, str(salt), str(key)))
    con.commit()


def login_get_salt(login):
    # Получение "соли" по имени пользователя
    ret = list(cur.execute(fr'SELECT salt FROM login WHERE name = ?', (login, )))
    if len(ret) > 0:
        return ret[0][0]


def login(login, key):
    # Вход с возвратом ключа авторизации
    ret = list(cur.execute(fr'SELECT name FROM login WHERE name = ? AND key = ?', (login, str(key))))
    if len(ret) > 0:
        id = str(uuid.uuid4())
        cur.execute(fr'DELETE FROM keys WHERE name = ?', (login, ))
        cur.execute(fr'INSERT INTO keys (name, key) VALUES (?, ?)', (login, id))
        return id


def add_row(key, name, about, file_name):
    # Добавление данных в таблицу
    ret = list(cur.execute(fr'SELECT name FROM keys WHERE key = ?', (key, )))
    if len(ret) > 0:
        author = ret[0][0]
        s = 'INSERT INTO data(author, name, about, file_name, file) VALUES(?, ?, ?, ?, ?)'
        if file_name == '#None#':
            data = (author, name, about, None, None)
        else:
            data = (author, name, about, file_name, open(file_name, 'rb').read())
        cur.execute(s, data)
        con.commit()
        os.remove(file_name)


def get_all_rows(key):
    # Получение всех данных пользователя по его ключу
    ret = list(cur.execute('SELECT name FROM keys WHERE key = ?', (key,)))
    if len(ret) > 0:
        ret = cur.execute('SELECT name, time, about, file_name FROM data WHERE author = ?', (ret[0][0], ))
        return list(ret)


def get_file(key, date):
    # Получение файла пользователя по его ключу и времени сохранения
    ret = list(cur.execute('SELECT name FROM keys WHERE key = ?', (key,)))
    if len(ret) > 0:

        s = 'SELECT file_name, file FROM data WHERE author = ? AND time = ?'
        flt = '0987654321 :-'
        data = (ret[0][0], ''.join(list(filter(lambda x: x in flt, date))))

        ret = list(cur.execute(s, data))
        if len(ret):
            return ret[0]


sock = socket.socket()
sock.bind(('', 20951))
log_file = open('server.log', 'a+')
while True:
    sock.listen(1)
    conn, addr = sock.accept()
    data_list = []
    data = conn.recv(1024)
    if data:
        try:
            data = data.decode('utf-8')

            log_file.write(str(datetime.datetime.today()) + " ||| " + data + '\n')
            log_file.flush()
            os.fsync(log_file.fileno())

            data = shlex.split(data)
            if data[0] == 'reg_check_login':
                if not reg_check_login(data[1]):
                    conn.send(b'False')
                else:
                    conn.send(b'True')
            elif data[0] == 'reg':
                reg(data[1], data[2], data[3])
            elif data[0] == 'login_get_salt':
                s = login_get_salt(data[1])
                if s:
                    conn.send(s.encode('utf-8'))
            elif data[0] == 'login':
                s = login(data[1], data[2])
                if s:
                    conn.send(s.encode('utf-8'))
            elif data[0] == 'add_row':
                key = data[1]
                name = data[2]
                about = data[3]
                file_name = data[4]
                if file_name != '#None#':
                    file = open(file_name, 'wb')
                    while True:
                        data = conn.recv(1024)
                        file.write(data)
                        if not data:
                            break
                    file.close()
                add_row(key, name, about, file_name)
            elif data[0] == 'get_all_rows':
                key = data[1]
                ret = qte(str(get_all_rows(key))).encode('utf-8')
                conn.send(ret)
            elif data[0] == 'get_file':
                ret = get_file(data[1], data[2])
                file = open(ret[0], 'wb')
                file.write(ret[1])
                file.close()
                with open(ret[0], 'rb') as file:
                    data = file.read(1024)
                    while data:
                        conn.send(data)
                        data = file.read(1024)
                    file.close()
                conn.send(b'')
                conn.close()
                os.remove(ret[0])
        except Exception as err:
            log_file.write('===================================\n' +
                           str(datetime.datetime.today()) + ' ||| ' + str(err) +
                           '\n===================================\n')
            log_file.flush()
            os.fsync(log_file.fileno())
