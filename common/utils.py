import time
import copy


def timeExecute(method):
    def timed(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        print(
            "Time execution of '{}' function is: {} ms".format(
                method.__name__, (end - start) * 1000
            )
        )
        return result

    return timed


def cacheDict(method):
    cacheTable = dict()

    def cached(*args, **kwargs):
        # key = "".join(k for k in args[1].values())
        # key.join(k for k in args[1].keys())
        key = id(args[1])
        # print(key)
        if key in cacheTable:
            return cacheTable[key]
        else:
            res = method(*args, **kwargs)
            cacheTable[key] = res
            return res

    return cached

