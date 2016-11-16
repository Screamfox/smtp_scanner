#!/usr/bin/python3

# def f(x): return x*x
def f(x): print(x*x)

import threading

# x.start()
# x.is_alive()
# x.join()

threading.TIMEOUT_MAX = 1

i = 0
j = 0
x = threading.Thread(target=f, args=([0]), kwargs={})
y = threading.Thread(target=f, args=([0]), kwargs={})
while(True):
    if not x.is_alive() and i <= 100: 
        x = threading.Thread(target=f, args=([i]), kwargs={})
        x.start()
        i += 1
    else:
        x.join()

    if not y.is_alive() and j <= 100:
        y = threading.Thread(target=f, args=([j]), kwargs={})
        y.start()
        j += 1
    else:
        y.join()
    
    if i >= 101 and j >= 101:
        # print(str(x.is_alive) +" and "+ str(y.is_alive))
        if x.is_alive and y.is_alive:
            break