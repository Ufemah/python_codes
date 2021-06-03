import socketserver
import shutil
import os
import sqlite3

server_path = 'server_data'
HOST = 'localhost'
PORT = 20001
code_d = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 0: 'zero'}


class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print('---------')
        print('connected from', self.client_address)
        data = self.rfile.readline().strip()
        print(data)

        if data == b'login':
            self.login()
        elif data == b'add user':
            self.add_user()
        elif data == b'send file':
            self.server_get_file_from_user()
        elif data == b'get file':
            self.server_send_file_to_user()
        elif data == b'get path':
            self.server_path()
        elif data == b'delete file or path':
            self.delete_file_or_path()
        elif data == b'add path':
            self.add_path()

        print('disconnected', self.client_address)

    def login(self):
        name = str(self.rfile.readline().strip(), encoding='utf-8')
        password = str(self.rfile.readline().strip(), encoding='utf-8')

        conn = sqlite3.connect('cloud.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM main WHERE Login=='{}' and Password == '{}'".format(name, password))
        get = cursor.fetchone()
        conn.close()
        print(get)
        print(name, password)
        if str(type(get)) == "<class 'NoneType'>":
            self.wfile.write(bytes('None', encoding='utf-8') + b'\n')

        else:
            result = str(get[0])
            send = ''
            lst = list(map(int, list(result)))
            for el in lst:
                send += code_d[el]
            send += ' ' + str(get[-1])
            print(send)
            self.wfile.write(bytes(send, encoding='utf-8') + b'\n')

    def add_user(self):
        name = str(self.rfile.readline().strip(), encoding='utf-8')
        password = str(self.rfile.readline().strip(), encoding='utf-8')
        print(name, password)

        conn = sqlite3.connect('cloud.db')
        cursor = conn.cursor()
        try:
            cursor.execute("insert into main values (Null, '{0}', '{1}', '0') ".format(str(name), str(password)))
            self.wfile.write(bytes('all right', encoding='utf-8') + b'\n')
        except sqlite3.IntegrityError:
            self.wfile.write(bytes('already created', encoding='utf-8') + b'\n')
        conn.commit()
        conn.close()

        conn = sqlite3.connect('cloud.db')
        cursor = conn.cursor()

        cursor.execute("SELECT Num FROM main WHERE Login=='{}' and Password == '{}'".format(name, password))
        get = cursor.fetchone()[0]
        conn.close()

        number = ''
        print(get)
        for i in str(get):
            number += code_d[int(i)]
        os.mkdir(server_path + '/' + number)

    def server_path(self):
        folder = str(self.rfile.readline().strip(), encoding='utf-8')
        print('path:', list(folder))
        files = []
        paths = []
        for (path, name, filename) in os.walk(server_path + '/' + folder):
            files.extend(filename)
            paths.extend(name)
            break
        print(files, paths)

        path_send = ''
        for i in paths:
            path_send += i + '*****'
        self.wfile.write(bytes(path_send, encoding='utf-8') + b'\n')

        files_send = ''
        for i in files:
            files_send += i + '*****'
        self.wfile.write(bytes(files_send, encoding='utf-8') + b'\n')

    def add_path(self):
        path_name = str(self.rfile.readline().strip(), encoding='utf-8')
        print(path_name)
        os.makedirs(server_path + '/' + path_name)

    def delete_file_or_path(self):
        file_name = str(self.rfile.readline().strip(), encoding='utf-8')
        print(file_name)
        try:
            os.remove(server_path + '/' + file_name)
        except PermissionError:
            shutil.rmtree(server_path + '/' + file_name)
        except IsADirectoryError:
            os.rmdir(server_path + '/' + file_name)

    def server_get_file_from_user(self):
        try:
            file_name = str(self.rfile.readline().strip(), encoding='utf-8')
            f = open(server_path + '/' + file_name, "wb")
            print(file_name)

            data = self.rfile.read(1024)
            while data:
                f.write(data)
                data = self.rfile.read(1024)

            f.close()
        except FileNotFoundError:
            pass

    def server_send_file_to_user(self):
        try:
            file_name = str(self.rfile.readline().strip(), encoding='utf-8')
            print(file_name)

            f = open(server_path + '/' + file_name, "rb")
            to_send = f.read(1024)
            while to_send:
                self.wfile.write(to_send)
                to_send = f.read(1024)

            f.close()
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    print('=== Drive server ===')
    socketserver.TCPServer((HOST, PORT), RequestHandler).serve_forever()
