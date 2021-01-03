#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .bracket import *
from .bracket.utils import pairwise
from enum import Enum
import os, random

path = os.path.dirname(os.path.realpath(__file__)) + "/"
default_alpha_path = lambda: path + 'data/alpha_defaults.csv'
base_alpha_path = lambda rnd: path + 'data/alpha' + str(rnd.value) + '.csv'

file_map = { Regions.EAST: path + "data/data_east.csv",
            Regions.WEST: path + "data/data_west.csv",
            Regions.SOUTH: path + "data/data_south.csv",
            Regions.MIDWEST: path+"data/data_midwest.csv"
        }

class Bracket(object):
    '''
    Defines a tournament bracket.
    '''
    def __init__(self):
        self.alphas = Alpha(base_alpha_path)
        self.default_alphas = DefaultAlpha(default_alpha_path)
        self.regions = (Region(file_map[Regions.MIDWEST], Regions.MIDWEST, self.alphas, self.default_alphas), 
            Region(file_map[Regions.WEST], Regions.WEST, self.alphas, self.default_alphas),
            Region(file_map[Regions.EAST], Regions.EAST, self.alphas, self.default_alphas), 
            Region(file_map[Regions.SOUTH], Regions.SOUTH, self.alphas, self.default_alphas)
        )
        self.rounds = { rnd: [] for rnd in Round }
        self.winner = self.run()

    def alpha(self, rnd: Round, s1: int, s2: int):
        try:
            return self.alphas.get_alpha(rnd, s1, s2)
        except:
            return self.default_alphas.get_alpha(rnd)

    def run(self) -> Team:
        # Rounds 1 - 4
        for region in self.regions:
            rnd = Round.ROUND_OF_64
            while rnd.value < Round.FINAL_4.value:
                self.rounds[rnd].extend(region.rounds[rnd])
                rnd = Round(rnd.value + 1)
        
        # Round 5 (Final 4)
        for pair in pairwise(self.regions):
            self.rounds[Round.FINAL_4].append(Match(pair[0].winner, pair[1].winner, 
                self.alpha(Round.FINAL_4, pair[0].winner, pair[1].winner)))
        
        
        # Round 6 (Championship)
        self.rounds[Round.CHAMPIONSHIP].append(Match(self.rounds[Round.FINAL_4][0].winner, 
            self.rounds[Round.FINAL_4][1].winner,
            self.alpha(Round.CHAMPIONSHIP, self.rounds[Round.FINAL_4][0].winner.seed, 
                self.rounds[Round.FINAL_4][1].winner.seed)))

        return self.rounds[Round.CHAMPIONSHIP][0].winner

    def __dict__(self):
        return { rnd.value: self.rounds[rnd] for rnd in self.rounds }
    
    def __str__(self):
        return str({ rnd.name: [str(match) for match in self.rounds[rnd]] for rnd in self.rounds})
    