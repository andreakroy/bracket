from round import Rounds
import random

class Sample:
    '''
    Initializes
    '''
    def __init__(self):
        self.round_counts = { round: [] for round in Rounds }
        self.observed_counts = [57,29,17,13,7,3,3,5,1,1,4,0,0,0,0,0] # Observed counts of Final Four Appearances


    '''
    Returns a probability from the probability mass function
    of the truncated geometric distribution.

    Attributes
    ----------
    round (int) - the round for which the probability is desired.
    seed (int) - the seed for which the probability is desired.
    '''
    def get_pmf(self) -> list:
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

    def run(self):
        print(self.get_pmf())
 

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
        self.get_pmf()
        self.pmf = self.round_counts[Rounds.FINAL_4]
        self.cdf = []

    def get_seeds(self):
        seeds = []
        total = 0

        for i in range(len(self.pmf)):
            total += self.pmf[i]
            self.cdf.append(total)
            

        for i in range(4):
            r = random.random()
            absolute_difference_function = lambda list_value : abs(list_value - r)

            closest_value = min(self.pmf, key=absolute_difference_function)
            ind = self.pmf.index(closest_value)
            seeds.append(ind + 1)
        return seeds

if __name__ == "__main__":
    #y = Sample()
    #print(y.run())
    x = F4_A()
    print(x.get_seeds())
'''
class E_8(Sample):
    
    Defines an E_8 sampling function; returns 8 seeds for the Elite 8.

    Attributes
    ----------
    seed (int) - the team's tournament seed in the range [1, 16].
    name (str) - the team's name.
    
    def __init__(self):

'''
        