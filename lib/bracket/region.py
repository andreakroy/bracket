from csv import reader
from enum import Enum
from .alpha import alpha_fn
from .match import Match
from .round import Rounds
from .team import Team
from .utils import matchorder, pairwise
from .sample import * 

class Regions(Enum):
    '''
    Enum defining the four regions in the tournament.
    '''
    WEST = 0
    EAST = 1
    MIDWEST = 2
    SOUTH = 3

class Region:
    '''
    Defines a region with 16 teams in the tournament.

    Attributes
    ----------
    teams (dict) : a dict with seed number -> Team for each of the sixteen teams in the region.
    rounds (dict) : a dict with Rounds -> list of Match objects for each of the six rounds in the tournament.
    region (Regions) : an enum value representing one of the four possible Regions.
    alpha_fn (callable) : a function to look up alpha values (see alpha.py).
    winner (Team) : stores the winning Team in the region (AKA the winner of the Elite Eight Matchup
        in a particular region).
    '''
    def __init__(self, file_path: str, region: Regions, alpha_fn: callable, 
        sample_seeds: list=None, sample_round: Rounds=None):
        '''
        Constructs a Region object.

        Parameters
        ----------
        file_path (str) : a path to a .csv file storing the first round matchup data.
        region (Regions) : a Regions enum value storing the region.
        alpha_fn (callable) : a function to look up alpha values (see alpha.py).
        '''
        self.teams = {}
        self.rounds = { rnd: [] for rnd in Rounds if rnd.value < Rounds.FINAL_4.value }
        self.region = region
        self.alpha_fn = alpha_fn
        self.sample_seeds = sample_seeds
        self.sample_round = sample_round

        # extract all teams from the data file.
        with open(file_path, 'r') as f:
            csv_reader = reader(f)  
            for seed, name in csv_reader:
                s = int(seed)
                self.teams[s] = Team(s, name)
        
        # initialize known first round matchups.
        for s1, s2 in pairwise(matchorder):
            self.rounds[Rounds.ROUND_OF_64].append(Match(self.teams[s1], 
                self.teams[s2], Rounds.ROUND_OF_64, self.alpha_fn))
        
        # run this region of the bracket and calculate the winner.
        self.winner = self.run()

    def run(self) -> Team:
        '''
        Returns the winning team in the region and fills in all the matches played.
        ''' 
        # Start at the round of 32 b/c the round of 64 is initialized from the file data.
        rnd = Rounds.ROUND_OF_32

        while rnd.value < Rounds.FINAL_4.value:
            # Each match is formed from the winners of the previous two matches,
            for m1, m2 in pairwise(self.rounds[Rounds(rnd.value - 1)]):
                t1 = m1.winner
                t2 = m2.winner
                winner = None
                if rnd.value <= self.sample_round:
                    if t1 in self.sample_seeds:
                        winner = t1
                    elif t2 in self.sample_seeds:
                        winner = t2
                self.rounds[rnd].append(Match(t1, t2, rnd, winner, self.alpha_fn))
                
            rnd = Rounds(rnd.value + 1)
            
        # the winner is the winner of the Elite Eight matchup.
        return self.rounds[Rounds.ELITE_8][0].winner
