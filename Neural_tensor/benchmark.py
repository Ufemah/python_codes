import functools


def benchmark(f):
    import datetime

    @functools.wraps(f)
    def _benchmark(*args, **kw):
        t = datetime.datetime.now()
        res = f(*args, **kw)
        t = datetime.datetime.now() - t
        print('\n\n\n{0} time elapsed {1}\n\n\n'.format(f.__name__, t))
        return res
    return _benchmark


if __name__ == "__main__":
    @benchmark
    def name():
        for i in range(20):
            print(i)

    name()
