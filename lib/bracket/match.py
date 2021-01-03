from .team import Team
import random
class Match(object):
    '''
    Defines one game between two teams.

    Attributes
    ----------
    t1 (Team) - Team name representing one team in the game.
    t2 (Team) - Team name representing the other team in the game.
    a
    '''
    
    def __init__(self, team1: Team, team2: Team, alpha: float):
        '''
        Constructs a match object.
        '''
        self.t1 = team1
        self.t2 = team2
        self.alpha = alpha
        self.prob = self.win_prob() if self.alpha != None else None
        self.winner = self.get_winner() if self.prob else None

    def win_prob(self) -> float:
        return (1.0 * self.t2.seed ** self.alpha) / (self.t1.seed ** self.alpha + self.t2.seed ** self.alpha)

    def get_winner(self):
        '''
        Returns the winning Team object. Returns None if self.prob is None.
        '''
        rand = random.random() 
        return self.t1 if rand < self.prob else self.t2
        
    def __str__(self):
        '''
        Returns a string representation of a Match.
        '''
        return f'{self.t1} vs. {self.t2} winner: {self.winner}'