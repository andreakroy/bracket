#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .bracket import *
from .bracket.utils import pairwise
from enum import Enum
import json, os, random

class Bracket(object, samplingFunction):
    '''
    Defines a tournament bracket.
    '''
    def __init__(self):
        self.af = alpha_fn(Alpha(base_alpha_path), DefaultAlpha(default_alpha_path))
        self.regions = (Region(data_files[0], Regions.MIDWEST, self.af), 
            Region(data_files[1], Regions.WEST, self.af),
            Region(data_files[2], Regions.EAST, self.af), 
            Region(data_files[3], Regions.SOUTH, self.af)
        )
        self.rounds = { rnd: [] for rnd in Rounds }
        self.winner = self.run()

    def run(self) -> Team:
        # Rounds 1 - 4
        for region in self.regions:
            rnd = Rounds.ROUND_OF_64
            while rnd.value < Rounds.FINAL_4.value:
                self.rounds[rnd].extend(region.rounds[rnd])
                rnd = Rounds(rnd.value + 1)
        
        # Rounds 5 (Final 4)
        for pair in pairwise(self.regions):
            self.rounds[Rounds.FINAL_4].append(Match(pair[0].winner, pair[1].winner, 
                Rounds.FINAL_4, self.af))
        
        
        # Rounds 6 (Championship)
        self.rounds[Rounds.CHAMPIONSHIP].append(
            Match(self.rounds[Rounds.FINAL_4][0].winner, self.rounds[Rounds.FINAL_4][1].winner,
                Rounds.CHAMPIONSHIP, self.af))

        return self.rounds[Rounds.CHAMPIONSHIP][0].winner

    def to_json(self):
        '''
        Returns a json serializeable dict representation of a Bracket.
        '''
        d = {
            'winner': self.winner.to_json()
        }
        d.update({ rnd.value: [match.to_json() for match in self.rounds[rnd]] for rnd in self.rounds})
        return d