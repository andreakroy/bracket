#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import csv
import os

path = os.path.dirname(os.path.realpath(__file__)) + '/'

def get_alphas(rndnum) -> dict:
    alphas = {}
    with open(path + 'data/alpha' + str(rndnum) + '.csv', 'r') as data:
        reader = csv.reader(data)
        for line in reader:
            alphas[set((line[0], line[1]))] = line[2]
    return alphas

def get_default_alphas() -> dict:
    alphas = {}
    with open(path + 'data/alpha_defaults.csv', 'r') as data:
        reader = csv.reader(data)
        for line in reader:
            alphas[set((line[0], line[1]))] = line[2]
    return alphas
