from csv import reader
from enum import Enum
from .utils import matchorder, pairwise
from .alpha import alpha, Alpha, DefaultAlpha
from .team import Team
from .round import Round
from .match import Match

class Regions(Enum):
    '''
    Enum defining the four regions in the tournament.
    '''
    WEST = 0,
    EAST = 1,
    MIDWEST = 2,
    SOUTH = 3

class Region:
    '''
    Defines a region with 16 teams in the tournament.

    Attributes
    ----------
    teams (dict) - a dict seed number -> name of the sixteen teams in the region.
    region (Regions) - an enum value representing one of the four possible Regions.
    '''
    def __init__(self, file_path: str, region: Regions, alphas: Alpha, default_alphas: DefaultAlpha):
        '''
        Constructs a Region object.
        '''
        self.teams = {}
        self.rounds = { rnd: [] for rnd in Round }
        self.region = region
        self.alpha = alpha(alphas, default_alphas)
        with open(file_path, 'r') as f:
            csv_reader = reader(f)
            # extract all teams from the data file
            for seed, name in csv_reader:
                s = int(seed)
                self.teams[s] = Team(s, name)
        
        # initialize known first round matchups
        for s1, s2 in pairwise(matchorder):
            self.rounds[Round.ROUND_OF_64].append(Match(self.teams[s1], 
                self.teams[s2], self.alpha(Round.ROUND_OF_64, s1, s2)))
        self.winner = self.run()

    def run(self) -> Team:
        rnd = Round.ROUND_OF_32
        while rnd.value < Round.FINAL_4.value:
            for m1, m2 in pairwise(self.rounds[Round(rnd.value - 1)]):
                t1 = m1.winner
                t2 = m2.winner
                self.rounds[rnd].append(Match(t1, t2, self.alpha(rnd, t1.seed, t2.seed)))
            rnd = Round(rnd.value + 1)
        return self.rounds[Round.ELITE_8][0].winner
        