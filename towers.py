import tkinter as tk


class Towers:
    def __init__(self, n):

        self.in_progress = False
        self.button_flag = False
        self.move_from = -1
        self.move_to = -1
        self.n = n

        self.columns = [[], [], []]
        self.dict = {i: 0 for i in range(1, n + 1)}

        self.root = tk.Tk()
        self.root.title("Hanoi towers")

        self.can = tk.Canvas(self.root, height=600, width=1000, bg='#27AE60')
        self.can.pack()
        self.can.create_rectangle(162.5, 600 - (n * 40 + 20), 187.5, 600, fil='#5F6A6A')
        self.can.create_rectangle(487.5, 600 - (n * 40 + 20), 512.5, 600, fil='#5F6A6A')
        self.can.create_rectangle(812.5, 600 - (n * 40 + 20), 837.5, 600, fil='#5F6A6A')

        for r in range(1, n + 1):
            l1 = 65 + (r - 1) * 10
            l2 = 600 - (r - 1) * 40
            l3 = 285 - (r - 1) * 10
            l4 = 560 - (r - 1) * 40
            self.dict[r] = self.can.create_rectangle(l1, l2, l3, l4, fil='#F1C40F')
            self.columns[0].append(r)

        self.can.bind("<Button-1>", self.key_down)

    def key_down(self, key):
        if not self.in_progress:
            self.in_progress = True
            if not self.button_flag:
                self.move_from = key.x // 325

                self.button_flag = True
                try:
                    self.move_up(self.columns[self.move_from][-1])
                except IndexError:
                    pass
                self.in_progress = False
            else:
                self.in_progress = True
                self.move_to = key.x // 325

                if len(self.columns[self.move_to]) != 0:
                    if self.columns[self.move_from][-1] < self.columns[self.move_to][-1]:
                        self.move_to = self.move_from

                try:
                    self.move(self.columns[self.move_from][-1])
                    self.move_down(self.columns[self.move_from][-1])
                    self.columns[self.move_to].append(self.columns[self.move_from][-1])
                    self.columns[self.move_from] = self.columns[self.move_from][:-1]
                except IndexError:
                    pass
                self.button_flag = False
                self.in_progress = False

                # print(self.columns)
                if len(self.columns[1]) == self.n or len(self.columns[2]) == self.n:
                    print("You win!")

    def move(self, obj):
        if self.move_from < self.move_to:
            pos = self.can.coords(self.dict[obj])
            if (pos[2] - pos[0]) / 2 + pos[0] < self.move_to * 325 + 175:
                self.can.move(self.dict[obj], 5, 0)
                self.can.update()
                self.can.after(1)
                self.move(obj)

        elif self.move_from > self.move_to:
            pos = self.can.coords(self.dict[obj])
            if (pos[2] - pos[0]) / 2 + pos[0] > self.move_to * 325 + 175:
                self.can.move(self.dict[obj], -5, 0)
                self.can.update()
                self.can.after(1)
                self.move(obj)
        else:
            pass

    def move_up(self, obj):
        pos = self.can.coords(self.dict[obj])
        if pos[1] > 100:
            self.can.move(self.dict[obj], 0, -5)
            self.can.update()
            self.can.after(1)
            self.move_up(obj)

    def move_down(self, obj):
        pos = self.can.coords(self.dict[obj])

        length = len(self.columns[self.move_to])
        if self.move_to != self.move_from:
            length += 1

        if pos[1] < 600 - length * 40:
            self.can.move(self.dict[obj], 0, 5)
            self.can.update()
            self.can.after(1)
            self.move_down(obj)

    def play(self):
        self.can.focus_set()
        self.root.mainloop()


if __name__ == "__main__":
    k = 9

    if k > 9:
        print("k-value is too big")
    else:
        Towers(k).play()
