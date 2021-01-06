#!/home/bracketodds/Python-2.7.8/python
# -*- coding: UTF-8 -*-

import cgi
from lib.database import generateJSON
from lib.bracket.sample import *

x = E_8()
gen = x()
for i in gen:
    print(i)