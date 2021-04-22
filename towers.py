import tkinter as tk


class Towers:
    def __init__(self, n):

        self.in_progress = False
        self.button_flag = False
        self.move_from = -1
        self.move_to = -1
        self.n = n
        self.count = 0
        self.speed = 20
        self.delay = 10
        self.size = self.height, self.width = 600, 1000

        self.columns = [[], [], []]
        self.dict = {i: 0 for i in range(1, n + 1)}
        self.text_dict = self.dict.copy()

        self.root = tk.Tk()
        self.root.title("Hanoi towers")

        self.can = tk.Canvas(self.root, height=self.height, width=self.width, bg='#27AE60')
        self.can.pack()
        self.can.create_rectangle(147.5, 600 - (n * 40 + 20), 172.5, 600, fil='#5F6A6A')
        self.can.create_rectangle(487.5, 600 - (n * 40 + 20), 512.5, 600, fil='#5F6A6A')
        self.can.create_rectangle(827.5, 600 - (n * 40 + 20), 852.5, 600, fil='#5F6A6A')

        for r in range(1, n + 1):
            l1 = 50 + (r - 1) * 10
            l2 = 600 - (r - 1) * 40
            l3 = 270 - (r - 1) * 10
            l4 = 560 - (r - 1) * 40
            self.dict[r] = self.can.create_rectangle(l1, l2, l3, l4, fil='#F1C40F')
            self.text_dict[r] = self.can.create_text(161, (l2 + l4) / 2, text=n - r + 1)
            self.columns[0].append(r)

        self.moves_count = self.can.create_text(75, 15, fill="black", font="Arial 20", text="Moves: 0")

        self.can.bind("<Button-1>", self.key_down)

    def key_down(self, key):
        if not self.in_progress:
            self.in_progress = True
            if not self.button_flag:
                self.move_from = key.x // 334

                self.button_flag = True
                try:
                    self.move_up(self.columns[self.move_from][-1])
                except IndexError:
                    self.in_progress = False

            else:
                self.in_progress = True
                self.move_to = key.x // 334

                print(self.move_from, self.move_to)

                if len(self.columns[self.move_to]) != 0 and len(self.columns[self.move_from]) != 0:
                    if self.columns[self.move_from][-1] < self.columns[self.move_to][-1]:
                        self.move_to = self.move_from

                try:
                    self.move_side(self.columns[self.move_from][-1])
                    self.columns[self.move_to].append(self.columns[self.move_from][-1])
                    self.columns[self.move_from] = self.columns[self.move_from][:-1]

                    self.count += 1
                    self.can.itemconfigure(self.moves_count, text="Moves: {}".format(self.count))
                except IndexError:
                    self.in_progress = False

                self.button_flag = False

                if len(self.columns[1]) == self.n or len(self.columns[2]) == self.n:
                    self.can.create_text(500, 300, fill="black", font="Arial 40", text="You win!")
                    self.in_progress = True

    def move_side(self, obj):
        if self.move_from < self.move_to:
            pos = self.can.coords(self.dict[obj])
            if (pos[2] - pos[0]) / 2 + pos[0] < self.move_to * 330 + 170:
                self.can.move(self.dict[obj], self.speed, 0)
                self.can.move(self.text_dict[obj], self.speed, 0)
                self.can.update()
                self.can.after(self.delay, self.move_side, obj)
            else:
                self.can.after(self.delay, self.move_down, obj)

        elif self.move_from > self.move_to:
            pos = self.can.coords(self.dict[obj])
            if (pos[2] - pos[0]) / 2 + pos[0] > self.move_to * 330 + 170:
                self.can.move(self.dict[obj], -self.speed, 0)
                self.can.move(self.text_dict[obj], -self.speed, 0)
                self.can.update()
                self.can.after(self.delay, self.move_side, obj)
            else:
                self.can.after(self.delay, self.move_down, obj)

        else:
            self.can.after(self.delay, self.move_down, obj)

    def move_up(self, obj):
        pos = self.can.coords(self.dict[obj])
        if pos[1] > 100:
            self.can.move(self.dict[obj], 0, -self.speed)
            self.can.move(self.text_dict[obj], 0, -self.speed)
            self.can.update()
            self.can.after(self.delay, self.move_up, obj)
        else:
            self.in_progress = False

    def move_down(self, obj):
        pos = self.can.coords(self.dict[obj])
        if pos[1] < self.height - len(self.columns[self.move_to]) * 40:
            self.can.move(self.dict[obj], 0, self.speed)
            self.can.move(self.text_dict[obj], 0, self.speed)
            self.can.update()
            self.can.after(self.delay, self.move_down, obj)
        else:
            self.in_progress = False

    def play(self):
        self.can.focus_set()
        self.root.mainloop()


if __name__ == "__main__":
    k = 9

    if k > 9:
        print("k-value is too big")
    else:
        Towers(k).play()
