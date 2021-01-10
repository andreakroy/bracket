#!/home/bracketodds/Python-2.7.8/python
# -*- coding: UTF-8 -*-

import cgi
from lib.bracket.sample import F4_A, E_8
from lib.database import generateJSON

x = generateJSON(samplingFunction=E_8())

f = F4_A()

check = { i: 0 for i in range(1, 17) }
for _ in range(100000):
    gen = f()
    for lst in gen:
        for val in lst:
            check[val] += 1

pmf_sim = { i : check[i] / sum(check.values()) for i in check}
print(pmf_sim)