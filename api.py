#!/home/bracketodds/Python-2.7.8/python
# -*- coding: UTF-8 -*-

import cgi
from lib.bracket.sample import F4_A, E_8
from lib.database import generateJSON

x = generateJSON(samplingFunction=E_8())
print(x)