#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from os.path import dirname, realpath

# an iterator for pairwise iteration. 
# [a, b, c, d, e, f] : (a, b) -> (c, d) -> (e, f)
def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

# The order of seeds (pairwise) in which the matches are played
matchorder = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]

# The base file path
path = dirname(dirname(realpath(__file__))) + "/"

# Function which returns the default alpha file path.
default_alpha_path = lambda: path + 'data/alpha_defaults.csv'

# Function which given a round, returns the alpha file path for that round.
base_alpha_path = lambda rnd: path + 'data/alpha' + str(rnd.value) + '.csv'

# File paths to the matchup data for the four regions.
data_files = [path + 'data/data_east.csv',
            path + 'data/data_west.csv',
            path + 'data/data_south.csv',
            path + 'data/data_midwest.csv'
]

# File paths to the round appearance data for all 16 seeds.
sample_data_files = [path + 'bracket/sample/data/round4.csv',
            path + 'bracket/sample/data/round5.csv',
            path + 'bracket/sample/data/round6.csv'
]
