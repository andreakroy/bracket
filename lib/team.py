#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Team:
    def __init__(self, seed, name=None):
        # seed - integer [1, 16]
        # name - str
        self.seed = seed
        self.name = name

    def __dict__(self):
        return {'seed' : self.seed, 'name' : self.name}

    def __str__(self):
        return f'[{self.seed}] ' + self.name
