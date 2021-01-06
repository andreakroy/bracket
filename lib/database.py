#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.bracket import bracket
import os
import json
from .bracket.sample import F4_A, E_8

def generateJSON(uniqueID=None, samplingFunction=None):
    # returns an HTML string

    b = bracket.Bracket()
    return b.to_json()