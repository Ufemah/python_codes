from tkinter import filedialog
from functools import partial
import tkinter as tk
import hashlib
import socket


HOST = 'localhost'
PORT = 20001
folder_icon = '📂'


class Log:
    def __init__(self):
        self.name = None
        self.password = None
        self.path_id = None

        self.root = tk.Tk()
        self.root.geometry("370x240+150+150")
        self.root.iconbitmap('icon.ico')
        self.root.title('Login')

        tk.Label(text="Login", font="Arial, 15").grid(row=1, column=0)
        name = tk.Entry(width=50)
        name.grid(row=2, column=1, columnspan=3)

        password = tk.Entry(width=50, show='*')
        password.grid(row=3, column=1, columnspan=3)

        tk.Label(text="username:").grid(row=2, column=0)
        tk.Label(text="password:").grid(row=3, column=0)

        tk.Button(text="Login", command=partial(self.quit, name, password)).grid(row=4, column=2)
        tk.Button(text="Create new account", command=self.new_user).grid(row=5, column=2)

        self.root.mainloop()

    def quit(self, name, password):
        self.name = name.get()
        h = hashlib.sha1()
        h.update(bytes(password.get(), encoding='utf-8'))
        self.password = h.hexdigest()
        self.test_user()
        if self.path_id != 'None\n':
            self.root.destroy()
        else:
            tk.Label(text="Wrong login or password").grid(row=6, column=2)

    def test_user(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        inp = s.makefile('rb', 0)
        out = s.makefile('wb', 0)

        out.write(bytes('login', encoding='utf-8') + b'\n')
        out.write(bytes(self.name, encoding='utf-8') + b'\n')
        out.write(bytes(self.password, encoding='utf-8') + b'\n')

        self.path_id = str(inp.readline(), encoding='utf-8')

        s.shutdown(2)
        s.close()

    def new_user(self):
        children = tk.Toplevel(self.root)
        children.title("Register")
        children.iconbitmap('icon.ico')
        children.geometry("385x240+100+100")

        tk.Label(children, text="Register", font="Arial, 12").grid(row=0, column=0)

        tk.Label(children, text="username:").grid(row=1, column=0)
        name = tk.Entry(children, width=43)
        name.grid(row=1, column=1, columnspan=3)

        tk.Label(children, text="password:").grid(row=2, column=0)
        password1 = tk.Entry(children, width=43, show='*')
        password1.grid(row=2, column=1, columnspan=3)

        tk.Label(children, text="repeat password:").grid(row=3, column=0)
        password2 = tk.Entry(children, width=43, show='*')
        password2.grid(row=3, column=1, columnspan=3)

        label_fields = tk.Label(children, text="all fields are necessary")
        label_passwords = tk.Label(children, text="passwords must be the same")
        label_created = tk.Label(children, text="account created")
        label_created_error = tk.Label(children, text="account has been already created")

        tk.Button(children, text="Register", command=partial(self.quit_reg, children, name, label_created,
                                                             label_created_error, label_fields, label_passwords,
                                                             password1, password2)).grid(row=4, column=2)

    @staticmethod
    def quit_reg(children, name, label_created, label_created_error, label_fields, label_passwords,
                 password1, password2):

        name = name.get()
        password1 = password1.get()
        password2 = password2.get()

        if any(el == '' for el in [name, password2, password1]):
            label_passwords.grid_remove()
            label_created_error.grid_remove()
            label_fields.grid(row=6, column=2)

        elif password2 != password1:
            label_fields.grid_remove()
            label_created_error.grid_remove()
            label_passwords.grid(row=6, column=2)

        else:
            label_fields.grid_remove()
            label_passwords.grid_remove()
            label_created_error.grid_remove()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))

            inp = s.makefile('rb', 0)
            out = s.makefile('wb', 0)

            out.write(bytes('add user', encoding='utf-8') + b'\n')

            out.write(bytes(name, encoding='utf-8') + b'\n')

            h = hashlib.sha1()
            h.update(bytes(password1, encoding='utf-8'))
            out.write(bytes(h.hexdigest(), encoding='utf-8') + b'\n')

            answer = str(inp.readline().strip(), encoding='utf-8')
            print(answer)

            s.shutdown(2)
            s.close()

            if answer == 'all right':
                label_created.grid(row=6, column=2)
                tk.Button(children, text="Quit", command=children.destroy).grid(row=7, column=2)
            elif answer == 'already created':
                label_created_error.grid(row=6, column=2)


class Main:
    def __init__(self, _id, admin):
        self.is_admin = admin
        if self.is_admin == 1:
            self.greet_admin()

        self.id = _id
        self.folder = _id
        self.test = None

        self.root = tk.Tk()
        self.root.geometry("720x480+300+300")
        self.root.iconbitmap('icon.ico')
        self.root.title('Cloud storage')

        self.lst_box = tk.Listbox(selectmode=tk.EXTENDED, width=90, height=30)

        self.lst_box.pack(side=tk.LEFT)

        self.refresh()
        scroll = tk.Scrollbar(command=self.lst_box.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.lst_box.config(yscrollcommand=scroll.set)

        f = tk.Frame()
        f.pack(side=tk.LEFT, padx=10)
        button = tk.Button(f, text="Add new file", command=self.send_file_to_server, width=25, height=4)
        button.pack(fill=tk.X)

        button = tk.Button(f, text="Save file", command=self.get_file_from_server, width=25, height=4)
        button.pack(fill=tk.X)

        button = tk.Button(f, text="Delete", command=self.delete_file_or_path, width=25, height=4)
        button.pack(fill=tk.X)

        button = tk.Button(f, text="Add new folder", command=self.add_folder, width=25, height=4)
        button.pack(fill=tk.X)

        button = tk.Button(f, text="Open folder", command=self.open_folder, width=25, height=4)
        button.pack(fill=tk.X)

        button = tk.Button(f, text="Back", command=self.back_folder, width=25, height=4)
        button.pack(fill=tk.X)

        self.root.mainloop()

    def greet_admin(self):
        root1 = tk.Tk()
        root1.geometry("400x80+150+150")
        root1.iconbitmap('icon.ico')
        root1.title('Error')

        label_one = tk.Label(root1, text='Hello, admin')
        label_one.config(font=("Arial", 20))
        label_one.pack()
        root1.after(1000, lambda: root1.destroy())
        root1.mainloop()

    def refresh(self):
        self.lst_box.delete(0, tk.END)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        inp = s.makefile('rb', 0)
        out = s.makefile('wb', 0)

        out.write(bytes('get path', encoding='utf-8') + b'\n')
        out.write(bytes(self.folder, encoding='utf-8') + b'\n')

        paths = str(inp.readline(), encoding='utf-8').split('*****')
        files = str(inp.readline(), encoding='utf-8').split('*****')

        s.shutdown(2)
        s.close()

        for i in reversed(files):
            if i != '\n':
                self.lst_box.insert(0, i)

        for i in reversed(paths):
            if i != '\n':
                self.lst_box.insert(0, folder_icon + i)

    def some_stuff(self, entry, window):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        out = s.makefile('wb', 0)

        out.write(bytes('add path', encoding='utf-8') + b'\n')
        out.write(bytes(self.folder + '\\' + str(entry.get()), encoding='utf-8') + b'\n')

        window.destroy()
        self.refresh()

    def add_folder(self):
        window = tk.Toplevel()
        window.geometry("360x120+350+350")
        window.title('New folder')
        window.iconbitmap('icon.ico')

        label = tk.Label(window, text='Input folder name', width=25, height=4)
        label.pack()

        entry = tk.Entry(window)
        entry.pack()

        button = tk.Button(window, text="Add this", width=25, height=4, command=partial(self.some_stuff, entry, window))
        button.pack(fill=tk.X)

    def open_folder(self):
        try:
            select = list(self.lst_box.curselection())
            file_name = self.lst_box.get(0, tk.END)[int(select[0])]
            if folder_icon in file_name:
                self.folder = self.folder + '\\' + file_name.replace(folder_icon, '')
                self.refresh()
        except IndexError:
            pass

    def back_folder(self):
        if self.folder != self.id or self.is_admin == 1:
            self.folder = '\\'.join(self.folder.split('\\')[0:-1])
        self.refresh()

    def delete_file_or_path(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        out = s.makefile('wb', 0)

        out.write(bytes('delete file or path', encoding='utf-8') + b'\n')

        select = list(self.lst_box.curselection())
        try:
            file_name = self.lst_box.get(0, tk.END)[int(select[0])].replace(folder_icon, '')
            out.write(bytes(self.folder + '\\' + file_name, encoding='utf-8') + b'\n')

            self.refresh()
            print(file_name, 'deleted')
        except IndexError:
            pass

    def send_file_to_server(self):
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        file_path = str(filedialog.askopenfilename()).replace('/', '\\')
        file_name = file_path.split("\\")[-1]

        if folder_icon not in file_name:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))

            out = s.makefile('wb', 0)

            out.write(bytes('send file', encoding='utf-8') + b'\n')

            out.write(bytes(self.folder + '\\' + file_name, encoding='utf-8') + b'\n')  # send file name to server
            try:
                file_send = open(file_path, "rb")
                to_send = file_send.read(1024)
                while to_send:
                    out.write(to_send)
                    to_send = file_send.read(1024)
                file_send.close()

                print(file_name, 'send')

            except FileNotFoundError:
                pass

            s.shutdown(2)
            s.close()
            self.refresh()
        else:
            root1 = tk.Tk()
            root1.geometry("400x80+150+150")
            root1.iconbitmap('icon.ico')
            root1.title('Error')

            label_one = tk.Label(root1, text='You can\'t use forbidden symbols')
            label_one.config(font=("Arial", 20))
            label_one.pack()
            root1.after(1000, lambda: root1.destroy())
            root1.mainloop()

    def get_file_from_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        inp = s.makefile('rb', 0)
        out = s.makefile('wb', 0)
        try:
            select = list(self.lst_box.curselection())
            file_name = self.lst_box.get(0, tk.END)[int(select[0])]

            if folder_icon in file_name:
                pass
            else:
                out.write(bytes('get file', encoding='utf-8') + b'\n')
                out.write(bytes(self.folder + '\\' + file_name, encoding='utf-8') + b'\n')

                root = tk.Tk()
                root.withdraw()
                root.wm_attributes('-topmost', 1)

                file_path = filedialog.asksaveasfilename(initialfile=file_name).replace('/', '\\')

                try:
                    file_get = open(file_path, "wb")
                    get = inp.read()
                    while get:
                        file_get.write(get)
                        get = inp.read()
                    file_get.close()

                    print(file_path.split('\\')[-1], 'saved')

                except FileNotFoundError:
                    pass

                s.shutdown(2)
                s.close()
        except IndexError:
            pass


if __name__ == '__main__':
    log = Log()
    try:
        if log.path_id.strip() != 'None':
            got = log.path_id.strip().split()
            print('path =', got[0])
            main = Main(got[0], int(got[1]))
    except AttributeError:
        pass
