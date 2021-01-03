#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import csv
import os
from .round import Round
from .team import Team

class DefaultAlpha:
    '''
    Class to store the default alpha values for each round in memory.
    '''
    def __init__(self, path_fn: callable):
        self.alphas = {}
        with open(path_fn(), 'r') as data:
            reader = csv.reader(data)
            for rnd, alpha in reader:
                self.alphas[Round(int(rnd))] = float(alpha)
    
    def get_alpha(self, rnd: Round) -> float:
        '''
        Returns the default alpha value for a particular round.
        Raises a KeyError if an invalid rnd argument is provided.

        Parameters
        ----------
        rnd (Round) : a valid Enum value representing the round.
        '''
        return self.alphas[rnd]

class Alpha:
    def __init__(self, path_fn: callable):
        self.alphas = {}
        for rnd in Round:
            self.alphas[rnd] = {}
            with open(path_fn(rnd), 'r') as data:
                reader = csv.reader(data)
                for s1, s2, alpha in reader:
                    self.alphas[rnd][tuple(sorted((int(s1), int(s2))))] = float(alpha)

    def get_alpha(self, rnd: Round, s1: int, s2: int) -> float:
        return self.alphas[rnd][tuple(sorted((s1, s2)))]

def alpha(alpha: Alpha, default_alpha: DefaultAlpha):
    def alpha_(rnd: Round, s1: int, s2: int):
        try:
            return alpha.alphas[rnd][tuple(sorted((s1, s2)))]
        except:
            return default_alpha.alphas[rnd]
    return alpha_