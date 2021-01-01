from csv import reader
from enum import Enum
from team import Team


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
    teams (list) - a list of the sixteen teams in the region.
    region (Regions) - an enum value representing one of the four possible Regions.
    '''
    def __init__(self, file_path: str, region: Regions):
        '''
        Constructs a Region object.
        '''
        self.teams = []
        self.region = region
        with open(file_path, 'r') as f:
            csv_reader = reader(f)
            for row in csv_reader:
                self.teams.append(Team(*row))
        
