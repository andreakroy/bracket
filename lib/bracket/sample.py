import random
import numpy as np
from .round import Rounds
from .utils import sample_path, matchorder
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
    adjustments (dict) : a map of adjusted seeds onto a tuple with adjusted number of ocurrences and adjusted probability.
    '''
    def __init__(self, rnd: Rounds, seed: int=None, adjustments: dict=None):
        '''
        Constructs a Sample for a given round.

        Parameters
        ----------
        rnd (Rounds) : the round for which the Sample is used.
        '''
        self.rnd = rnd 
        self.rng = np.random.default_rng(seed)
        self.adjustments = adjustments
        self.observed_counts = self.get_observed_counts()
        self.adjust_counts(self.adjustments)

    def __call__(self) -> list:
        '''
        Sample callable function. Returns a sampled list of seeds that survive up till a given round.
        '''
        pass

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

    def get_pmf(self) -> list:
        # calculate q parameter for the truncated geometric distribution.
        q = 0
        for seed, count in self.observed_counts.items():
            q += (count * seed)
        q /= sum(self.observed_counts.values())
        q = 1 / q
        k = 1 / (1 - (1 - q)**(len(self.observed_counts)))
        pmf = [ k * q * (1 - q)**(i - 1) for i in self.observed_counts ]
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
        t = toml.load(sample_path)
        adjustments = { int(seed) : (int(new_count), float(prob)) for seed, [new_count, prob] in t['F4_A'].items() }
        Sample.__init__(self, Rounds.FINAL_4, seed, adjustments)

    def __call__(self):
        '''
        Returns 4 sampled seeds for the Final Four.
        '''
        # the number of seeds to generate with the pmf. Starts with 4 and then is decremented everytime a seed is sampled
        # in stage 1.
        num = 4
        # initial sampling procedure using adjustments
        for seed, (_, prob) in self.adjustments.items():
            if random.random() < prob:
                num -= 1
                yield[seed]
        # Sample the remaining number of seeds in the range [1, 16] according to the pmf.
        for i in self.rng.choice(np.arange(1, 17), num, p=self.get_pmf()):
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
        t = toml.load(sample_path)
        adjustments = { int(seed) : (int(new_count), float(prob)) for seed, [new_count, prob] in t['E_8'].items() }
        Sample.__init__(self, Rounds.ELITE_8, seed, adjustments)

    def __call__(self):
        '''
        Returns 8 seeds for the Elite 8.
        '''
        top_half_seeds = matchorder[:8]
        bottom_half_seeds = matchorder[8:]
        pmf = self.get_pmf()
        top_half_pmf = [ pmf[seed - 1] for seed in top_half_seeds ]
        bottom_half_pmf = top_half_pmf = [ pmf[seed - 1] for seed in bottom_half_seeds ]

        top_half_pmf = [ float(i) / sum(top_half_pmf) for i in top_half_pmf ]
        bottom_half_pmf = [ float(i) / sum(bottom_half_pmf) for i in bottom_half_pmf ]

        # initial sample size from top and bottom halves. Decreases as seeds are sampled in stage 1.
        bottom_num, top_num = 4, 4

        # initial sampling procedure using adjustments
        for seed, (_, prob) in self.adjustments.items():
            if random.random() < prob:
                if seed in top_half_seeds:
                    top_num -= 1
                else:
                    bottom_num -= 1
                yield[seed]

        tops = self.rng.choice(top_half_seeds, bottom_num, p=top_half_pmf)
        bottoms = self.rng.choice(bottom_half_seeds, top_num, p=bottom_half_pmf)

        # secondary sampling with geometric pmh        
        for i in range(len(tops)):
            yield [tops[i], bottoms[i]]