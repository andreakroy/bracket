#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Team:
    '''
    Defines a single team in the tournament.

    Attributes
    ----------
    seed (int) - the team's tournament seed in the range [1, 16].
    name (str) - the team's name
    '''
    def __init__(self, seed: int, name: str):
        '''
        Constructs a Team object
        '''
        self.seed = seed
        self.name = name

    def __dict__(self):
        '''
        Returns a dict represenatiton of a Team object.
        '''
        return {'seed' : self.seed, 'name' : self.name}

    def __str__(self):
        '''
        Returns a str representation of a Team object.
        '''
        return f'[{self.seed}] ' + self.name
