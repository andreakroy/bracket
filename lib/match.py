from team import Team
from enum import Enum

class Match(object):
    '''
    Defines one game between two teams.

    Attributes
    ----------
    t1 (Team) - Team name representing one team in the game.
    t2 (Team) - Team name representing the other team in the game.
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
    
    def __init__(self, team1: Team, team2: Team, state: State=State.UNKNOWN):
        '''
        Constructs a match object.
        '''
        self.t1 = team1
        self.t2 = team2
        self.state = state

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