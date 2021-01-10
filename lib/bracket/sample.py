import random
import numpy as np
from .round import Rounds
from .utils import *
import toml

class Sample:
    '''
    Initializes a callable Sample. Calling the sample yields a list of seeds that
    must win (and survive up to) the Sample round.

    Attributes
    ----------
    rnd (Rounds) : the round enum valyue for which the sampling function is used.
    pmf (int) : the Probability Mass Function for each seed reaching a given round.
    rng (np.random.Generator) : a random number generator.
    adjusted_seeds (dict) : a map of adjusted seeds onto to the adjusted number of ocurrences.
    '''
    def __init__(self, rnd: Rounds, seed: int=None, adjusted_seeds: dict=None):
        '''
        Constructs a Sample for a given round.

        Parameters
        ----------
        rnd (Rounds) : the round for which the Sample is used.
        '''
        self.rnd = rnd 
        self.rng = np.random.default_rng(seed)
        self.adjusted_seeds = adjusted_seeds
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
        # extract all teams from the data file.
        t = toml.load(sample_path)

        # observed counts of appearances in the sample round for each seed.
        observed_counts = { int(seed) : count for seed, count in t[str(self.rnd.value)].items() }

        # calculate q parameter for the truncated geometric distribution.
        q = 0
        for seed, count in observed_counts.items():
            q += (count * seed)
        q /= sum(observed_counts.values())
        q = 1 / q
        k = 1 / (1 - (1 - q)**(len(observed_counts)))
        pmf = [k * q * (1 - q)**(i - 1) for i in observed_counts]
        return [val / sum(pmf) for val in pmf]

class F4_A(Sample):
    '''
    Defines an F4_A sampling function. 

    Attributes
    ----------
    Sample
    '''
    def __init__(self, seed: int=None):
        '''
        Constructs an F4_A Sample.
        '''
        Sample.__init__(self, Rounds.FINAL_4, seed, {11 : 1})

    def __call__(self):
        '''
        Returns 4 sampled seeds for the Final Four.
        '''
        # Sample seeds in the range [1, 16] according to the pmf.
        for i in self.rng.choice(np.arange(1, 17), 4, p=self.pmf):
            yield [i]

class E_8(Sample):
    '''
    Defines an E_8 sampling function.

    Attributes
    ----------  
    Sample
    '''
    def __init__(self, seed=None):
        '''
        Constructs an E_8 Sample.
        '''
        Sample.__init__(self, Rounds.ELITE_8, seed, {1: 1, 11: 1})

    def __call__(self):
        '''
        Returns 8 seeds for the Elite 8.
        '''
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
            yield [tops[i], bottoms[i]]