#!/home/bracketodds/Python-2.7.8/python
# -*- coding: UTF-8 -*-

import cgi
from lib.bracket import BracketType
from lib.bracket.sample import F4_A
from lib.database import generateJSON
from lib.bracket.round import Rounds

x = generateJSON(bracket_type=BracketType.WOMEN)
print(x)
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