def readData(path):
    with open(path) as data:
        yield from map(str.strip, data)

def timeIt(func):
    def timed(*args, **kwargs):
        from time import time
        st = time()
        result = func(*args, **kwargs)
        print("%s took %0.2fs" % (func.__name__, round(time()-st, 2)))
        return result
    return timed