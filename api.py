#!/home/bracketodds/Python-2.7.8/python
# -*- coding: UTF-8 -*-

import cgi
from lib.bracket import BracketType
from lib.bracket.sample import F4_A, E_8
from lib.database import generateJSON
from lib.bracket.round import Rounds
from lib.bracket.utils import *

f = E_8()
#print(f())
seeds_top = {i : 0 for i in top}
seeds_bottom = {i : 0 for i in bottom}
for _ in range(10000):
    for ls in f():
        for l in ls:
            if l in seeds_top:
                seeds_top[l] += 1
            if l in seeds_bottom:
                seeds_bottom[l] += 1
                
print({i : seeds_top[i] for i in seeds_top})
print({i : seeds_bottom[i] for i in seeds_bottom})
print({i : seeds_top[i] / sum(seeds_top.values()) for i in seeds_top})
a = {i : seeds_bottom[i] / sum(seeds_bottom.values()) for i in seeds_bottom}
print(a)
print(sum(a.values()))
#x = generateJSON(bracket_type=BracketType.MEN, sampling_fn=F4_A())
#print(x)
#print(generateJSON(samplingFunction=F4_A()))

""" s = F4_A()
seeds = {i : 0 for i in range(1, 17)}
for _ in range(100000):
    for ls in s():
        for l in ls:
            seeds[l] += 1

num_seeds = sum(seeds.values())
print({i : seeds[i] / num_seeds for i in seeds}) """

""" x = generateJSON(samplingFunction=E_8())

f = F4_A()

check = { i: 0 for i in range(1, 17) }
for _ in range(100000):
    gen = f()
    for lst in gen:
        for val in lst:
            check[val] += 1

pmf_sim = { i : check[i] / sum(check.values()) for i in check}
print(pmf_sim) """