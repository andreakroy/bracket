#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv, os
from .round import Rounds
from .team import Team

class Alpha:
    '''
    Stores the alpha values for each round in memory.
    '''
    def __init__(self, default_alpha_path: str, r1_alpha_path: str):
        '''
        Constructs a DefaultAlpha object to look up default alpha values by round.
        
        Parameters
        ----------
        default_alpha_path (str) : a file path for the default alpha file
        r1_alpha_path (callable) : a file path for the round 1 alpha file.
        '''
        self.default_alphas = {}
        self.r1_alphas = {}
        with open(default_alpha_path, 'r') as data:
            reader = csv.reader(data)
            for rnd, alpha in reader:
                self.default_alphas[Rounds(int(rnd))] = float(alpha)
        with open(r1_alpha_path, 'r') as data:
            reader = csv.reader(data)
            for s1, s2, alpha in reader:
                self.r1_alphas[tuple(sorted((int(s1), int(s2))))] = float(alpha)
    
    def get_alpha(self, rnd: Rounds, s1: int=None, s2: int=None) -> float:
        '''
        Returns the default alpha value for a particular round.
        Raises a KeyError if an invalid rnd argument is provided.

        Parameters
        ----------
        rnd (Rounds) : the round enum value.
        s1 (int) : the seed of t1 in a match pairing.
        s2 (int) : the seed of t2 in a match pairing.
        '''
        if rnd == Rounds.ROUND_OF_64:
            return self.r1_alphas[tuple(sorted((s1, s2)))]
        else:
            return self.default_alphas[rnd]