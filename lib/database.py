#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .tourney import Bracket
import os
import json

def generateJSON(uniqueID=None):
    # returns an HTML string

    b = Bracket()
    return json.dumps(b.to_json())