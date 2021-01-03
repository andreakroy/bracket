#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .bracket import Bracket, determineWinners
from .team import Team
import os
import json

def generateJSON(uniqueID=None):
    # returns an HTML string

    mustGenerateNewBracket = uniqueID is None
    b = Bracket()
    if mustGenerateNewBracket:
        bitstring = None
        determineWinners(b, bitstring)
        bitstring = bin(b.getBitRepresentation())[2:] # eliminate leading 0b
        timestamp = getTimestamp()
        success = False
    # TODO: uncomment database operations once Internal Server Error is resolved
        while not success:
            try:
                uniqueID = getUniqueID()
                insert(timestamp, uniqueID, bitstring)
                success = True
            except dbconnect.Error as e:
                if e[0] != 1062:  # error code 1062: duplicate ID
                    raise e
    else:
        timestamp, bitstring = select(uniqueID)
        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        determineWinners(b, bitstring)


    # calculate score
    score, gamesCorrectList = calculateScore(b)
    matcheslist = [[[team.getJSON() for team in match.getTeams()] for match in rnd] for rnd in b.getMatches()]
    return json.dumps({"bitstring": bitstring, "timestamp": timestamp, "uniqueID": uniqueID, "matches": matcheslist, "isNew": mustGenerateNewBracket, "score": score, "gamesCorrect": sum(gamesCorrectList), "gamesCorrectList": gamesCorrectList})