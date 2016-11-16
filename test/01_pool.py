#!/usr/bin/python3

def f(x): return x*x

from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=2)

async_result = pool.apply_async(f, ([10]))
return_val =+ async_result.get()