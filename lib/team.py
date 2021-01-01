#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import csv
import os

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

    def __dict__(self) -> dict:
        '''
        Returns a dict represenatiton of a Team object.
        '''
        return {'seed' : self.seed, 'name' : self.name}

    def __str__(self) -> str:
        '''
        Returns a str representation of a Team object.
        '''
        return f'[{self.seed}] ' + self.name

path = os.path.dirname(os.path.realpath(__file__)) + "/"

'''
The file paths for the four regions with 16 teams each.
Data files are csv of teams

Specifications:
First sixteen teams - South
Second sixteen teams - East
Third sixteen teams - Midwest
Fourth sixteen teams - West
Within each region: 1v16, 8v9, 5v12, 4v13, 6v11, 3v14, 7v10, 2v15
'''
files = [path + "data/data_UL.txt",
         path + "data/data_LL.txt",
         path + "data/data_LR.txt",
         path + "data/data_UR.txt"]