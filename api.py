#!/home/bracketodds/Python-2.7.8/python
# -*- coding: UTF-8 -*-

import cgi
from lib.bracket.sample import F4_A
from lib.database import generateJSON

x = generateJSON(samplingFunction=F4_A())
print(x)