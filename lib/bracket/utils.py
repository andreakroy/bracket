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

# The file path for the default alpha file.
default_alpha_path = path + 'data/alpha/alpha_defaults.csv'

# the file path for the round 1 alpha file.
r1_alpha_path = path + 'data/alpha/alpha_r1.csv'

# File paths to the matchup data for the four regions.
data_files = [path + 'data/matchup/data_midwest.csv',
            path + 'data/matchup/data_west.csv',
            path + 'data/matchup/data_east.csv',
            path + 'data/matchup/data_south.csv',
]

# File paths to the round appearance data for all 16 seeds.
sample_base_path = path + 'data/sample/round'
