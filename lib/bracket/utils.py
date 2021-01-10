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

# The file path for the alpha configuration file.
alpha_path = path + 'data/alpha.toml'

# the file path for the regions configuration file.
regions_path = path + 'data/regions.toml'

# File paths to the sample configuration file.
sample_path = path + 'data/sample.toml'