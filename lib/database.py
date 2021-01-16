#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.bracket import Bracket, BracketType
from lib.bracket.sample import Sample
import os
import json

def generateJSON(uid: int=None, bracket_type: BracketType=BracketType.MEN, sampling_fn: Sample=None):
    b = Bracket(bracket_type, sampling_fn)
    return b.to_json()