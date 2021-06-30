"""
Perform an approximate calculation of π.
To do this, calculate the perimeter of an equilateral polygon and use p = 2r*pi
"""

from math import sqrt, pi, sin, cos
import tkinter as tk


class CountPi:
    def __init__(self):
        # init vars for counting pi
        self.value = 0
        self.radius = 1
        self.side = sqrt(2) * self.radius
        self.sides_count = 2
        self.max_step = 200000

        # init tkinter vars
        self.delay = 2000
        self.window_size = self.height, self.width = 800, 800  # window size
        self.center = (400, 400)

        self.root = tk.Tk()
        self.root.title("Pi value")
        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width, bg='#FFFFFF')
        self.canvas.pack()

        self.pi_draw = self.canvas.create_text(160, 25, font="Arial 20", text="P / 2R = %.10f" % self.value)
        self.n_draw = self.canvas.create_text(75, 780, font="Arial 20", text="n = %d" % self.sides_count)
        self.true_pi_draw = self.canvas.create_text(660, 25, font="Arial 20", text="Pi = %.10f" % pi)
        self.line = self.canvas.create_polygon(self.center * 2)

        self.driver()

    def driver(self):
        # recursive call main after delay
        self.main()
        self.canvas.after(self.delay, self.driver)

    def main(self):
        # count pi value
        if self.sides_count < self.max_step:
            a = self.side / 2
            b = self.radius - sqrt(self.radius ** 2 - a ** 2)
            self.side = sqrt(a ** 2 + b ** 2)

            perimeter = self.sides_count * self.side * 4

            self.value = perimeter / (2 * self.radius)

            self.sides_count *= 2

        # create points to create polygon
        vertex = []

        for i in range(0, self.sides_count):
            vertex.append((self.center[1] + self.center[0] * cos((pi / self.sides_count * 2) * i) * 0.8,
                           self.center[1] + self.center[0] * sin((pi / self.sides_count * 2) * i) * 0.8))
        vertex.append(vertex[0])

        # update polygon and text
        self.canvas.delete(self.line)
        self.line = self.canvas.create_line(vertex)
        self.canvas.itemconfigure(self.pi_draw, text="P / 2R = %.10f" % self.value)
        self.canvas.itemconfigure(self.n_draw, text="n = %d" % self.sides_count)

    def show_animation(self):
        self.canvas.focus_set()
        self.root.mainloop()


if __name__ == "__main__":
    p = CountPi()
    p.show_animation()
