import time


def timeExecute(method):
    def timed(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        print("Time execution of {} is: {} ms".format(method, (end - start) * 1000))

    return timed


# something wrong at here !!!
def cacheDict(method):
    print("fsdfadsf")
    cacheTable = dict()

    def cached(*args, **kwargs):
        key = "".join(k for k in args[1].values())
        # key.join(k for k in args[1].keys())
        if key in cacheTable:
            print("cached ", args[1])
            return cacheTable[key]
        else:
            print("tinhtn  ", args[1])
            res = method(*args, **kwargs)
            cacheTable[key] = res
            print(cacheTable)
            print(res)
            print(cacheTable[key])
            return res

    print("kjkhhkh", cacheTable)
    return cached

