from round import Rounds
import random
import numpy as np

class Sample:
    '''
    Initializes
    '''
    def __init__(self):
        self.round_counts = { round: [] for round in Rounds }
        self.observed_counts = [57,29,17,13,7,3,3,5,1,1,4,0,0,0,0,0] # Observed counts of Final Four Appearances
        self.pmf = self.calculate_pmf()

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
        for seed in range(1, 17):
            q += (self.observed_counts[seed - 1] * seed)
        q /= sum(self.observed_counts)
        q = 1 / q
        I_MAX = 16
        k = 1 / (1 - (1 - q)**(I_MAX))

        pmf = []
        for i in range(1, I_MAX + 1):
            pmf.append(k * q * (1 - q)**(i - 1))

        self.round_counts[Rounds.FINAL_4] = pmf
        return pmf

class F4_A(Sample):
    '''
    Defines an F4_A sampling function; returns 4 seeds for the Final Four.

    Attributes
    ----------
    pmf (list) - the team's tournament seed in the range [1, 16].
    name (str) - the team's name.
    '''
    def __init__(self):
        Sample.__init__(self)
        self.pmf = self.round_counts[Rounds.FINAL_4]
        self.seeds = []

        rng = np.random.default_rng()
        self.seeds = rng.choice(16, 4, p=self.pmf)
        for i in range(len(self.seeds)):
            self.seeds[i] += 1


if __name__ == "__main__":
    #y = Sample()
    #print(y.run())
    x = F4_A()
    #x.get_seeds()
    print(x.pmf)
'''
class E_8(Sample):
    
    Defines an E_8 sampling function; returns 8 seeds for the Elite 8.

    Attributes
    ----------
    seed (int) - the team's tournament seed in the range [1, 16].
    name (str) - the team's name.
    
    def __init__(self):

'''
        