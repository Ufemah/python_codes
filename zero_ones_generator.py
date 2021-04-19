class Onez:
    def __init__(self, n):
        self.n = n
        self.res = []

    def gen(self, inp, n):
        if n == 0:
            self.res.append(inp)
            return

        if inp[-1] != "1":
            self.gen(inp + "1", n - 1)

        self.gen(inp + "0", n - 1)

    def generator(self):
        self.gen("1", self.n - 1)
        self.gen("0", self.n - 1)

        return self.res


if __name__ == "__main__":
    print(Onez(5).generator())
