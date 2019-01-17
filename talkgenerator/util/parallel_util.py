from multiprocessing import Process


# From https://stackoverflow.com/questions/7207309/python-how-can-i-run-python-functions-in-parallel
def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()
