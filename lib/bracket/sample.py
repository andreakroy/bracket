import random
import numpy as np
from .round import Rounds
from .utils import *
import csv

class Sample:
    '''
    Initializes a callable Sample. Calling the sample yields a list of seeds that
    must win (and survive up to) the Sample round.

    Attributes
    ----------
    rnd (Rounds) : The round enum valyue for which the sampling function is used.
    pmf (int) : The Probability Mass Function for each seed reaching a given round.
    rng (np.random.Generator) : A random number generator.
    '''
    def __init__(self, rnd: Rounds):
        '''
        Constructs a Sample for a given round.

        Parameters
        ----------
        rnd (Rounds) : the round for which the Sample is used.
        '''
        self.rnd = rnd 
        self.rng = np.random.default_rng()
        self.pmf = self.get_pmf()

    def __call__(self) -> list:
        '''
        Sample callable function. Returns a sampled list of seeds that survive up till a given round.
        '''
        pass

    def get_pmf(self) -> list:
        '''
        Reads in pmf data and returns a list with a pmf for a specific round.
        '''
        # observed counts of Final Four appearances for each team.
        observed_counts = [] 
        file_path = sample_base_path + str(self.rnd.value) + '.csv'

        # extract all teams from the data file.
        with open(file_path, 'r') as f:
            reader = csv.reader(f)  
            for seed_appearances in next(reader):
                observed_counts.append(int(seed_appearances))

        # calculate q parameter for the truncated geometric distribution.
        q = 0
        for i in range(len(observed_counts)):
            q += (observed_counts[i] * (i + 1))
        q /= sum(observed_counts)
        q = 1 / q
        k = 1 / (1 - (1 - q)**(len(observed_counts)))

        return [k * q * (1 - q)**i for i in range(len(observed_counts))]

class F4_A(Sample):
    '''
    Defines an F4_A sampling function. 

    Attributes
    ----------
    Sample
    '''
    def __init__(self):
        '''
        Constructs an F4_A Sample.
        '''
        Sample.__init__(self, Rounds.FINAL_4)

    def __call__(self):
        '''
        Returns 4 sampled seeds for the Final Four.
        '''
        seeds = []
        # Sample seeds in the range [1, 16] according to the pmf.
        seeds = self.rng.choice(np.arange(1, 17), 4, p=self.pmf)
        return seeds

class E_8(Sample):
    '''
    Defines an E_8 sampling function.

    Attributes
    ----------
    Sample
    '''
    def __init__(self):
        '''
        Constructs an E_8 Sample.
        '''
        Sample.__init__(self, Rounds.ELITE_8)
    def __call__(self):
        '''
        Returns 8 seeds for the Elite 8.
        '''
        seeds = []
        top_half_seeds = matchorder[:8]
        bottom_half_seeds = matchorder[8:]
        top_half_pmf = []
        bottom_half_pmf = []
        
        for seed in top_half_seeds:
            top_half_pmf.append(self.pmf[seed - 1])

        for seed in bottom_half_seeds:
            bottom_half_pmf.append(self.pmf[seed - 1])

        top_half_pmf = [float(i) / sum(top_half_pmf) for i in top_half_pmf]
        bottom_half_pmf = [float(i) / sum(bottom_half_pmf) for i in bottom_half_pmf]
        tops = self.rng.choice(top_half_seeds, 4, p=top_half_pmf)
        bottoms = self.rng.choice(bottom_half_seeds, 4, p=bottom_half_pmf)
        for i in range(len(tops)):
            yield tops[i]
            yield bottoms[i]