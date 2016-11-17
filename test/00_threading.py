#!/usr/bin/python3

###
#   Tried both parallel processing and
# multi-threading and I found that threads
# are just plain easier to implement than processes.
#
#   In this example I just made an f function which,
# like the start / main function, takes one argument 
# and doesn't return anything. All I now have to do
# is find a way (@get_host) on how to write the results
# to a file.
### 

import time
import random
import sys, os
# def f(x):
#     time.sleep(random.random()*10)
#     return x*x
    
def f(x):    
    time.sleep(random.random())
    print(x*x)

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

    if not y.is_alive() and j <= 100:
        y = threading.Thread(target=f, args=([j]), kwargs={})
        y.start()
        j += 1
    
    if i >= 101 and j >= 101:
        # print(str(x.is_alive) +" and "+ str(y.is_alive))
        if x.is_alive and y.is_alive:
            x.join()
            y.join()
            break
        