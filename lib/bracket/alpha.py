#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv, os
from .round import Rounds
from .team import Team

class DefaultAlpha:
    '''
    Stores the default alpha values for each round in memory.
    '''
    def __init__(self, path_fn: callable):
        '''
        Constructs a DefaultAlpha object to look up default alpha values by round.
        
        Parameters
        ----------
        
        path_fn (callable) : a function which returns the name of the file path 
            of the default alpha values file.
        '''
        self.alphas = {}
        with open(path_fn(), 'r') as data:
            reader = csv.reader(data)
            for rnd, alpha in reader:
                self.alphas[Rounds(int(rnd))] = float(alpha)
    
    def get_alpha(self, rnd: Rounds) -> float:
        '''
        Returns the default alpha value for a particular round.
        Raises a KeyError if an invalid rnd argument is provided.

        Parameters
        ----------
        rnd (Rounds) : a valid Enum value representing the round.
        '''
        return self.alphas[rnd]

class Alpha:
    '''
    Class to store a set of alpha values for a particular year.
    '''
    def __init__(self, path_fn: callable):
        '''
        Constructs an Alpha object to look up alpha values based on a pair of seeds and a round.
        
        Parameters
        ----------
        path_fn (callable) : a function which takes in a Rounds enum values and returns the name of 
            the file path of the alpha values file for that particular round.
        '''
        self.alphas = {}
        for rnd in Rounds:
            self.alphas[rnd] = {}
            with open(path_fn(rnd), 'r') as data:
                reader = csv.reader(data)
                for s1, s2, alpha in reader:
                    self.alphas[rnd][tuple(sorted((int(s1), int(s2))))] = float(alpha)

    def get_alpha(self, rnd: Rounds, s1: int, s2: int) -> float:
        return self.alphas[rnd][tuple(sorted((s1, s2)))]

def alpha_fn(alpha: Alpha, default_alpha: DefaultAlpha) -> callable:
    '''
    Returns a function which first looks up an alpha value and if not available looks up a default
    alpha value from an Alpha and DefaultAlpha object in that order.

    Parameters
    ----------
    alpha (Alpha) : an Alpha object storing alpha values in memory.
    default_alpha (DefaultAlpha) : a DefaultAlpha object storing default alpha values in memory. 
    '''
    def alpha_(rnd: Rounds, t1: Team, t2: Team) -> float:
        '''
        Function that returns an alpha value for a round and pair of seeds if available. If not, returns the 
        default alpha value for that particular round.

        Parameters
        ----------
        rnd (Rounds) : the round enum value.
        t1 (Team) : a team object representing the first team in a match pairing.
        t2 (Team) : a team object representing the second team in a match pairing.
        '''
        try:
            return alpha.alphas[rnd][tuple(sorted((t1.seed, t2.seed)))]
        except:
            return default_alpha.alphas[rnd]
    return alpha_