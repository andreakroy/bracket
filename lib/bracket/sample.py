import random
import numpy as np
from .round import Rounds
from .utils import sample_path, matchorder
import toml
from math import ceil, log

class Sample:
    '''
    Initializes a callable Sample. Calling the sample yields a list of seeds that
    must win (and survive up to) the Sample round.

    Attributes
    ----------
    rnd (Rounds) : the round enum valyue for which the sampling function is used.
    pmf (int) : the Probability Mass Function for each seed reaching a given round.
    rng (np.random.Generator) : a random number generator.
    adjustments (dict) : a map of adjusted seeds onto a tuple with adjusted number of ocurrences and adjusted probability.
    '''
    def __init__(self, rnd: Rounds, adjustments: dict=None, seed: int=None):
        '''
        Constructs a Sample for a given round.

        Parameters
        ----------
        rnd (Rounds) : the round for which the Sample is used.
        '''
        self.rnd = rnd
        if seed:
            self.rng = np.random.default_rng(seed)
        else:
            self.rng = np.random.default_rng()
        self.adjustments = adjustments
        self.observed_counts = self.get_observed_counts()
        self.adjust_counts(self.adjustments)

    def get_observed_counts(self) -> list:
        '''
        Reads in pmf data and returns a list with a pmf for a specific round.
        '''
        # extract all teams from the data file.
        t = toml.load(sample_path)

        # observed counts of appearances in the sample round for each seed.
        return { int(seed) : count for seed, count in t[str(self.rnd.value)].items() }

    def adjust_counts(self, adjustments: dict) -> None:
        '''
        Adjusts the expected counts.

        Parameters
        ----------
        adjustments (dict) : a map of seeds to adjust onto the new count.
        '''
        for seed, (new_count, _) in adjustments.items():
            self.observed_counts[seed] = new_count

    def get_qhat(self, support: list) -> float:
        q = 0
        # seeded = { seed: count if seed in support else 0 for seed, count in self.observed_counts.items() }
        for seed, count in self.observed_counts.items():
            q += (count * seed)
        q /= sum(self.observed_counts.values())
        return 1 / q

    def get_psum(self, qhat: float) -> float:
        return (1 - (1 - qhat)**(len(self.observed_counts)))

    def sample_seed(self, max_val: int, support: list, fixed: int=None):
        # stage 1: adjustment sample
        if fixed:
            if random.random() < self.adjustments[fixed][1]:
                return fixed

        # stage 2: truncated geometric sampling.
        qhat = self.get_qhat(support)
        psum = self.get_psum(qhat)
        
        u = random.random() * psum
        if max_val:
            return min(max_val, int(ceil(log(u) / log(1 - qhat))))

class F4_A(Sample):
    '''
    Defines an F4_A sampling function. 

    Attributes
    ----------
    Sample
    '''
    def __init__(self, rng_seed: int=None):
        '''
        Constructs an F4_A Sample.

        Parameters
        ----------
        rng_seed (int) : a seed to use for the random number generator.
        '''
        t = toml.load(sample_path)
        adjustments = { int(seed) : (int(new_count), float(prob)) for seed, [new_count, prob] in t['F4_A'].items() }
        Sample.__init__(self, Rounds.FINAL_4, adjustments, rng_seed)

    def __call__(self):
        '''
        Returns a list of 4 sample seed lists (with one seed) for the Final Four.
        '''
        return [[self.sample_seed(16, matchorder, 11)] for _ in range(4)]

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
        t = toml.load(sample_path)
        adjustments = { int(seed) : (int(new_count), float(prob)) for seed, [new_count, prob] in t['E_8'].items() }
        Sample.__init__(self, Rounds.ELITE_8, adjustments, seed)

    def __call__(self):
        '''
        Returns 8 seeds for the Elite 8.
        '''
        out = []
        for _ in range(4):
            top_half = matchorder[:8]
            bottom_half = matchorder[:8]
            s1 = self.sample_seed(8, top_half)
            s2 = self.sample_seed(8, bottom_half)
            out.append([top_half[s1 - 1], top_half[s2 - 1]])
        return out