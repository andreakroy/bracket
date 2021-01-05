from .round import Rounds
import random
import numpy as np
from .utils import *
from csv import reader

class Sample:
    '''
    Initializes
    '''
    def __init__(self, rnd: Rounds):
        self.rnd = rnd 
        self.pmf = [] # Probability mass function for each seed reaching a given round
        self.rng = np.random.default_rng()
        
        self.calculate_pmf()

    def __call__(self):
        pass

    '''
    Returns a probability from the probability mass function
    of the truncated geometric distribution.

    Attributes
    ----------
    round (int) - the round for which the probability is desired.
    seed (int) - the seed for which the probability is desired.
    '''
    def calculate_pmf(self) -> list:
        observed_counts = [] # Observed counts of Final Four Appearances
        file_path = utils.sample_base_path + str(self.rnd) + ".csv"

        # extract all teams from the data file.
        with open(file_path, 'r') as f:
            csv_reader = reader(f)  
            
            for seed_appearances in next(csv_reader):
                s = int(seed_appearances)
                observed_counts.append(s)

        q = 0
        for i in range(len(observed_counts)):
            seed = i + 1
            q += (observed_counts[i] * seed)

        q /= sum(observed_counts)
        q = 1 / q
        k = 1 / (1 - (1 - q)**(len(observed_counts)))

        for i in range(len(observed_counts)):
            self.pmf.append(k * q * (1 - q)**(i))


class F4_A(Sample):
    '''
    Defines an F4_A sampling function; returns 4 seeds for the Final Four.

    Attributes
    ----------
    pmf (list) - the team's tournament seed in the range [1, 16].
    name (str) - the team's name.
    '''
    def __init__(self):
        Sample.__init__(self, 5) # Round 5 (Final Four)

    def __call__(self):
        seeds = []
        seeds = self.rng.choice(np.arange(1, 17), 4, p=self.pmf) # TODO

        return seeds



class E_8(Sample):
    '''
    Defines an E_8 sampling function; returns 8 seeds for the Elite 8.

    Attributes
    ----------
    seed (int) - the team's tournament seed in the range [1, 16].
    name (str) - the team's name.
    '''
    def __init__(self):
        Sample.__init__(self, 4) # Round 4 (Elite Eight)
        
    def __call__(self):
        seeds = []
        top_half_seeds = utils.matchorder[:8]
        bottom_half_seeds = utils.matchorder[8:]
        top_half_pmf = []
        bottom_half_pmf = []
        
        for seed in top_half_seeds:
            top_half_pmf.append(self.pmf[seed - 1])

        for seed in bottom_half_seeds:
            bottom_half_pmf.append(self.pmf[seed - 1])

        top_half_pmf = [float(i) / sum(top_half_pmf) for i in top_half_pmf]
        bottom_half_pmf = [float(i) / sum(bottom_half_pmf) for i in bottom_half_pmf]

        seeds = self.rng.choice(top_half_seeds, 4, p=top_half_pmf)
        return np.hstack([seeds, (self.rng.choice(bottom_half_seeds, 4, p=bottom_half_pmf))])



if __name__ == "__main__":
    #y = Sample()
    #print(y.run())
    x = E_8()
    #x.get_seeds()
    print(x())
    # for path in utils.sample_data_files:
    #     samp = Sample(path)
    #     print(samp.observed_counts)