import tkinter as tk


class Towers:
    def __init__(self, n):
        self.speed = 20  # speed of moving
        self.delay = 10  # delay between frames
        self.size = self.height, self.width = 600, 1000   # window size
        
        self.in_progress = False  # if True -> player can't click
        self.button_flag = False  # if True -> move_from pin is chosen
        self.move_from = -1
        self.move_to = -1
        self.n = n
        self.count = 0

        self.columns = [[], [], []]   # pin
        self.dict = {i: 0 for i in range(1, n + 1)}   # dictionary that will keep rect objects
        self.text_dict = self.dict.copy()  # dictionary for rect numbers

        self.root = tk.Tk()
        self.root.title("Hanoi towers")

        self.can = tk.Canvas(self.root, height=self.height, width=self.width, bg='#27AE60')
        self.can.pack()

        # pins
        for i in range(0, 3):
            self.can.create_rectangle(147.5 + 340 * i, 600 - (n * 40 + 20),
                                      172.5 + 340 * i, 600, fil='#5F6A6A')

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

            self.in_progress = True   # prevent player from clicks during animation

            # choose move_from and move_up
            if not self.button_flag:
                self.move_from = key.x // 334  # number of column
                self.button_flag = True   # says that move_from is chosen

                # if move_from is empty -> do nothing
                # else move_up
                if len(self.columns[self.move_from]) != 0:
                    self.move_up(self.columns[self.move_from][-1])
                else:
                    self.in_progress = False
                    self.button_flag = False

            # choose move_to and move rect to destination (if condition)
            else:
                self.in_progress = True   # prevent player from clicks during animation

                self.move_to = key.x // 334

                # if destination pin rect is smaller -> just move_down
                if len(self.columns[self.move_to]) != 0 and len(self.columns[self.move_from]) != 0:
                    if self.columns[self.move_from][-1] < self.columns[self.move_to][-1]:
                        self.move_to = self.move_from

                # move rect from one pin to another
                self.move_side(self.columns[self.move_from][-1])
                self.columns[self.move_to].append(self.columns[self.move_from][-1])
                self.columns[self.move_from] = self.columns[self.move_from][:-1]

                # on-screen moves count
                self.count += 1
                self.can.itemconfigure(self.moves_count, text="Moves: {}".format(self.count))

                # allow player click
                self.button_flag = False

                # check if game is finished
                if len(self.columns[1]) == self.n or len(self.columns[2]) == self.n:
                    self.can.create_text(self.width / 2, self.height / 2, fill="black", font="Arial 40", text="You win!")
                    self.in_progress = True

    def move_side(self, obj):
        # move right
        if self.move_from < self.move_to:
            pos = self.can.coords(self.dict[obj])
            # if rect center on the left of destination pin -> move right
            if (pos[2] - pos[0]) / 2 + pos[0] < self.move_to * 330 + 170:
                self.can.move(self.dict[obj], self.speed, 0)
                self.can.move(self.text_dict[obj], self.speed, 0)
                self.can.update()
                self.can.after(self.delay, self.move_side, obj)
            # if rect at destination by X axis
            else:
                self.can.after(self.delay, self.move_down, obj)

        # move left
        elif self.move_from > self.move_to:
            pos = self.can.coords(self.dict[obj])
            # if rect center on the right of destination pin -> move left
            if (pos[2] - pos[0]) / 2 + pos[0] > self.move_to * 330 + 170:
                self.can.move(self.dict[obj], -self.speed, 0)
                self.can.move(self.text_dict[obj], -self.speed, 0)
                self.can.update()
                self.can.after(self.delay, self.move_side, obj)
            # if rect at destination by X axis
            else:
                self.can.after(self.delay, self.move_down, obj)

        # just move down
        else:
            self.can.after(self.delay, self.move_down, obj)

    def move_up(self, obj):
        if self.can.coords(self.dict[obj])[1] > 100:
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
    k = 3

    if k > 9:
        print("k-value is too big")
    else:
        Towers(k).play()
