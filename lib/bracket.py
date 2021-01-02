#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from region import Region, Regions
from match import Match
from team import Team
from alpha import getAlphaFile, getDefaultAlphas
from more_itertools import pairwise
from enum import Enum
import random, time, datetime, binascii, os

# From 2018:
# PERFECTBITSTRING = "1000000000000011000001100000010000010010100011110000101110001101"

# For 2019:

# R1:
# East: 01100010
# West: 01100010
# Midwest: 01001000
# South: 01110010

R1 = "01100010011000100100100001110010"

# East:  0111
# West:  0111
# Midw:  0011
# South: 0011

#R2 = "2222222222222222"
R2 = "0111011100110011"

# East: 01
# West: 00
# Midw: 11
# South: 00

#R3 = "22222222"
R3 = "01001100"
R4 = "1100"
R5 = "11"
R6 = "1"
PERFECTBITSTRING = "1" + R1 + R2 + R3 + R4 + R5 + R6



matchorder = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
path = os.path.dirname(os.path.realpath(__file__)) + "/"

file_map = { Regions.EAST: path + "data/data_e.csv",
            Regions.WEST: path + "data/data_w.csv",
            Regions.SOUTH: + path + "data/data_s.csv",
            Regions.MIDWEST: path+"data/data_mw.csv"
        }

class Bracket(object):
    '''
    Defines a tournament bracket.
    '''
    class Rounds(Enum):
        '''
        Defines the 6 Rounds in the tournament.
        '''
        ROUND_OF_64 = 1, 
        ROUND_OF_32 = 2,
        SWEET_16 = 3, 
        ELITE_8 = 4,
        FINAL_4 = 5,
        CHAMPIONSHIP = 6

    def __init__(self):
        self.regions = {
            Regions.EAST: Region(file_map[Regions.EAST], Regions.EAST), 
            Regions.WEST: Region(file_map[Regions.WEST], Regions.WEST),
            Regions.MIDWEST: Region(file_map[Regions.MIDWEST], Regions.MIDWEST),
            Regions.SOUTH: Region(file_map[Regions.SOUTH], Regions.SOUTH)
        }
        # each round is mapped to an integer:
        # Round of 64 = 1, Round of 32 = 2, Sweet 16 = 3, 
        # Elite 8 = 4, Final Four = 5, Championship Game = 6
        self.rounds = {}

        def match(round_num: int):
            if round_num == self.Rounds.ROUND_OF_64.value:
                thisround = []
                for region in self.regions.values():
                    for seed1, seed2 in pairwise(matchorder):
                        thisround.append(Match(region.teams[seed1], region.teams[seed2]))
                self.rounds[round_num] = thisround
            elif round_num < self.Rounds.CHAMPIONSHIP.value:
                thisround = []
                for region in self.regions.values():
                    for match1, match2 in pairwise(self.rounds[round_num - 1]):
                        thisround.append(Match(match1.winner(), match2.winner()))
                self.rounds[round_num] = thisround
                match(round_num + 1)
            else:
                return

            # recursively match all teams
            match(self.Rounds.ROUND_OF_64.value)

    def getBitRepresentation(self): # for storage in database
        result = "1" # force every bit to appear
        for rnd in self.rounds.values():
            for match in rnd:
                result += str(match.state)
        return int(result,2) # resulting bitstring is 64-bits long, including leading bit

# PROBABILITY FUNCTIONS
def win(team1, team2, rndnum):
    if random.random() < winProb(team1, team2, rndnum):
        return team1
    else:
        return team2
    # return (team1 if r < winProb(team1, team2, rnd) else team2)

def winProb(team1, team2, rndnum):
    a = alpha(team1, team2, rndnum)
    seed1 = int(team1.getSeed())
    seed2 = int(team2.getSeed())
    return 1.0 * seed2**a / (seed1**a + seed2**a)

def alpha(team1, team2, rndnum):
    alphas = getAlphaFile(rndnum)
    defaults = getDefaultAlphas()
    try:
        minSeed, maxSeed = sorted([int(team1.getSeed()), int(team2.getSeed())])
        a = alphas[(minSeed, maxSeed)]
        # print "Found alpha for {0}, {1}. It's {2}".format(minSeed, maxSeed, a)
        return a
    except KeyError:        
        try:
            # print "Using default alpha for round {0}".format(rndnum)
            return defaults[rndnum]
        except KeyError:
            # print "Cannot find an alpha or default value for {0}, {1} in round {2}".format(minSeed, maxSeed, rndnum)
            return 1

# RUN THROUGH BRACKET
def determineWinners(bracket, bitstring=None):
    # bitstring (long int) - a 64-bit bitstring starting with 1
    rndnum = 2
    if bitstring is None: # generate new bracket according to model
        for rnd in bracket.getMatches():
            for match in rnd:
                team1 = match.getChild1().getValue()
                team2 = match.getChild2().getValue()
                match.setValue(win(team1,team2,rndnum))
            rndnum += 1
    else: # generate new bracket according to bitstring
        bitpos = 1
        bits = str(bitstring)
        for rnd in bracket.getMatches():
            for match in rnd:
                currentBit = bits[bitpos]
                if bool(int(currentBit)):
                    match.setValue(match.getChild2().getValue())
                else:
                    match.setValue(match.getChild1().getValue())
                bitpos += 1
            rndnum += 1

def calculateScore(otherBracket):
    perfectBracket = Bracket(getTeams())
    determineWinners(perfectBracket, PERFECTBITSTRING)
    value = 10
    totalScore = 0
    gamesCorrectList = []
    matches = otherBracket.getMatches()
    # print "Perfect Bracket:\n" + perfectBracket.__str__()
    # print "Your Bracket:\n" + otherBracket.__str__()
    for rndindex, rnd in enumerate(perfectBracket.getMatches()):
        gamesCorrect = 0
        for matchindex, match in enumerate(rnd):
            perfectWinner = match.getWinner()
            # print "Perfect has:", perfectWinner
            winner = matches[rndindex][matchindex].getWinner()
            # print "Yours has:", winner
            if perfectWinner.getName() == winner.getName():
                # print "Match!", value
                if rndindex < 1:
                    totalScore += value
                    gamesCorrect += 1
        gamesCorrectList.append(gamesCorrect)
        value *= 2
    return (totalScore, gamesCorrectList)

def getTimestamp():
    return datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def getUniqueID():
    return binascii.b2a_hex(os.urandom(8))