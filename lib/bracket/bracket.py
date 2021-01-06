#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .sample import Sample
from enum import Enum
import json, os, random
from .alpha import *
from .match import Match
from .team import Team
from.region import Region, Regions
from .round import Rounds
from .utils import *

class Bracket:
    '''
    Defines a tournament bracket.
    '''
    def __init__(self, sampling_fn: Sample=None):
        self.af = alpha_fn(Alpha(base_alpha_path), DefaultAlpha(default_alpha_path))
        self.sample = sampling_fn
        # pass the sampling function to the region if the sample function is for a round played
        # inside a region.
        region_sample = self.sample if self.sample.rnd.value < Rounds.FINAL_4 else None
        # Order is important. MIDWEST is paired with WEST and EAST is paired with SOUTH
        # when iterating pairwise over the regions tuple.
        self.regions = (Region(data_files[0], Regions.MIDWEST, self.af, region_sample), 
            Region(data_files[1], Regions.WEST, self.af, region_sample),
            Region(data_files[2], Regions.EAST, self.af, region_sample), 
            Region(data_files[3], Regions.SOUTH, self.af, region_sample)
        )
        self.rounds = { Rounds.FINAL_4: [], Rounds.CHAMPIONSHIP: [] }
        self.winner = self.run()
        self.match_list = self.matches()

    def run(self) -> Team:
        # Rounds 1 - 4 handled in each region.
        # Round 5 (Final 4)
        for pair in pairwise(self.regions):
            self.rounds[Rounds.FINAL_4].append(Match(pair[0].winner, pair[1].winner, 
                Rounds.FINAL_4, self.af))
        # Round 6 (Championship)
        self.rounds[Rounds.CHAMPIONSHIP].append(
            Match(self.rounds[Rounds.FINAL_4][0].winner, self.rounds[Rounds.FINAL_4][1].winner,
                Rounds.CHAMPIONSHIP, self.af))
        return self.rounds[Rounds.CHAMPIONSHIP].pop().winner
    
    def bits(self) -> str:
        '''
        Return a bitstring representing the bracket.
        '''
        out = ['0'] * 64

        for i in range(len(self.match_list)):
            out[i] = str(self.match_list[i].bits())
        return ''.join(out)

    def matches(self) -> list:
        '''
        Return an ordered list of all matches played in a bracket.
        '''
        # The first four rounds handled inside each region.
        regional_rounds = range(1, 5)
        # The last two rounds played across regions.
        final_rounds = range(5, 7)
        out = []
        for rnd_num in regional_rounds:
            for region in self.regions:
                for match in region.rounds[Rounds(rnd_num)]:
                    out.append(match)
        for rnd in final_rounds:
            for match in self.rounds[Rounds(rnd)]:
                out.append(match)
        return out

    def to_json(self):
        '''
        Returns a json serializeable dict representation of a Bracket.
        '''
        d = {
            'bitstring': self.bits(),
            'matches' : [match.to_json() for match in self.matches()]
        }
        return d