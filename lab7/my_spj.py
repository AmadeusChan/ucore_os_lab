# my own special judge scripts used to check if correctly solved the philosophers problem

import sys
import os
import glob
import re

HUNGER = 0
EATING = 1
THINKING = 2

TIMES = 4
N = 5

print "now compiling..."
os.system("make> /dev/null")

'''
print "now running default scripts..."
os.system("make grade")
'''

print "\nnow running special judge..."
cases = glob.glob("./user/*.c")

for i in range(len(cases)):
    cases[i] = re.split(r"/", cases[i])[-1][:-2]

hit = 0

for case in cases:
    state = [THINKING] * N
    times = [0] * N
    flag = True
    reason = ""
    with open("." + case + ".log", "r") as f:
        while True:
            line = f.readline()
            if line == None or len(line) == 0:
                break

            if re.search(r"philosopher_condvar is eating", line) != None:
                x = int(line[len("Iter 4, No.")])
                if state[x] != EATING and state[(x + N - 1) % N] != EATING and state[(x + 1) % N] != EATING:
                    state[x] = EATING
                    times[x] += 1
                else:
                    flag = False
                    reason = "something wrong when eating: state[LEFT]:%s, STATE[x]:%s, STATE[RIGHT]:%s" % (state[(x + N - 1) % N], state[x], state[(x + 1) % N])
                    break

            if re.search(r"finished eating", line) != None:
                x = int(line[len("phi_put_forks_condvar: ")])
                if state[x] == EATING:
                    state[x] = THINKING
                else:
                    flag = False
                    reason = "something wrong when finished eating: STATE: %s" % (state[x])
                    break
        if flag:
            for i in range(N):
                if times[i] != TIMES:
                    flag = False
                    reason = "times not match, times[%s] = %s" % (i, times[i])
                    break
        if flag:
            hit += 1
            print "case " + case + ", result: OK"
        else:
            print "case " + case + ", result: WRONG, reason: " + reason

print "\ngrade: %s/%s" % (hit, len(cases))
