
import re

def f():
    i = 0
    while i < 1103:
        i += 1

f()

def inner(i):
    return i + 1

def inlined_call():
    i = 0
    while i < 1103:
        i = inner(i)

inlined_call()

def uninlined_call():
    s = 0
    for i in range(3):
        s += 1
    return s

def bridge():
    s = 0
    i = 0
    while i < 10000:
        if i % 2:
            s += uninlined_call()
        else:
            s += 1
        i += 1
    return s

bridge()

def inlined_str_stuff():
    s = [str(i) for i in range(3000)]
    for elem in s:
        re.search('3', elem)

inlined_str_stuff()

def double_loop():
    s = 0
    for i in range(10000):
        for k in range(100):
            s += i + k
    return s

double_loop()
