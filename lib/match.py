from .team import Team
import csv
from enum import Enum
from .bracket import Bracket
import os
import alpha

# base file path for the alpha data
path = os.path.dirname(os.path.realpath(__file__)) + "/"
base_alpha = path + 'data/alpha'

class Match(object):
    '''
    Defines one game between two teams.

    Attributes
    ----------
    t1 (Team) - Team name representing one team in the game.
    t2 (Team) - Team name representing the other team in the game.
    rnd (Bracket.Rounds) - Enum value representing the match's round.
    state (Match.State) - Enum representing who won the match, or None if unknown.
    '''
    class State(Enum):
        '''
        Defines the two possible states of a match.
        (1) Team 1 wins (2) Team 2 Wins (3) Unknown
        '''
        T1 = 0,
        T2 = 1,
        UNKNOWN = 2
    
    def __init__(self, team1: Team, team2: Team, alpha: float,
        rnd: Bracket.Rounds, state: State=State.UNKNOWN):
        '''
        Constructs a match object.
        '''
        self.t1 = team1
        self.t2 = team2
        self.alpha = alpha
        self.rnd = rnd
        self.state = state
        self.prob = self.win_prob()

    def win_prob(self) -> float:
        return (1.0 * self.t2.seed ** self.alpha) / (self.t1.seed ** self.alpha + self.t2.seed ** self.alpha)

    def winner(self):
        '''
        Returns the winning Team object. Returns None if the state of the match is UNKNOWN.
        '''
        if self.state == self.State.T1:
            return self.t1
        elif self.state == self.State.T2:
            return self.t2
        return None

    def loser(self):
        '''
        Returns the losing Team object. Returns None if the state of the match is UNKNOWN.
        '''
        if self.state == self.State.T1:
            return self.t2
        elif self.state == self.State.T2:
            return self.t1
        return None
        
    def __str__(self):
        '''
        Returns a string representation of a Match.
        '''
        return f'[{self.t1.name}] vs. [{self.t2.name}]. winner: []]'