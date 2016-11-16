#!/usr/bin/python3

import time, os
from multiprocessing import Pool, TimeoutError

def f():
    time.sleep(5)
    return "dick"

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        res = pool.apply_async(f)
        print(res.get(timeout=6))