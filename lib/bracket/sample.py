from round import Rounds
import random
import numpy as np
import utils
from csv import reader

class Sample:
    '''
    Initializes
    '''
    def __init__(self, file_path: str):
        self.round_counts = { round: [] for round in Rounds }
        self.observed_counts = [] # Observed counts of Final Four Appearances
        self.pmf = []
        

        # extract all teams from the data file.
        with open(file_path, 'r') as f:
            csv_reader = reader(f)  
            for line in csv_reader:
                for seed_appearances in line:
                    s = int(seed_appearances)
                    self.observed_counts.append(s)
                
        self.calculate_pmf()

        

    '''
    Returns a probability from the probability mass function
    of the truncated geometric distribution.

    Attributes
    ----------
    round (int) - the round for which the probability is desired.
    seed (int) - the seed for which the probability is desired.
    '''
    def calculate_pmf(self) -> list:
        q = 0
        for i in range(len(self.observed_counts)):
            seed = i + 1
            q += (self.observed_counts[i] * seed)
        q /= sum(self.observed_counts)
        q = 1 / q
        
        k = 1 / (1 - (1 - q)**(len(self.observed_counts)))

        for i in range(1, len(self.observed_counts) + 1):
            self.pmf.append(k * q * (1 - q)**(i - 1))

        self.round_counts[Rounds.FINAL_4] = self.pmf

class F4_A(Sample):
    '''
    Defines an F4_A sampling function; returns 4 seeds for the Final Four.

    Attributes
    ----------
    pmf (list) - the team's tournament seed in the range [1, 16].
    name (str) - the team's name.
    '''
    def __init__(self):
        Sample.__init__(self, utils.sample_data_files[1])
        #self.pmf = self.round_counts[Rounds.FINAL_4]
        self.seeds = []

        rng = np.random.default_rng()
        self.seeds = rng.choice(16, 4, p=self.pmf)
        for i in range(len(self.seeds)):
            self.seeds[i] += 1



class E_8(Sample):
    '''
    Defines an E_8 sampling function; returns 8 seeds for the Elite 8.

    Attributes
    ----------
    seed (int) - the team's tournament seed in the range [1, 16].
    name (str) - the team's name.
    '''
    def __init__(self):
        Sample.__init__(self, utils.sample_data_files[0])
        #self.pmf = self.round_counts[Rounds.FINAL_4]
        self.seeds = []

        rng = np.random.default_rng()
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

        self.seeds = rng.choice(top_half_seeds, 4, p=top_half_pmf)
        self.seeds = np.hstack([self.seeds, (rng.choice(bottom_half_seeds, 4, p=bottom_half_pmf))])



if __name__ == "__main__":
    #y = Sample()
    #print(y.run())
    x = E_8()
    #x.get_seeds()
    print(x.seeds)
    for path in utils.sample_data_files:
        samp = Sample(path)
        print(samp.observed_counts)