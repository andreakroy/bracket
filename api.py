#!/usr/bin/env python
from lib.bracket import Bracket, BracketType
from lib.bracket.sample import F4_A, E_8
from lib.database import getBracket
from lib.bracket.round import Rounds
from lib.bracket.utils import *
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/v1/', methods=['GET'])
def api():
    assert request.method == 'GET'
    args = request.args
    if 'uid' in args:
        uid = args['uid']
        return getBracket(uid)
        # TODO: check if the uid is in the database. If so return it.
    else:
        # Setting the men's bracket as the default since most users choose this.
        bt = BracketType.MEN
        if 'type' in args:
            try:
                bt = BracketType(args['type'])
            except:
                return 'Invalid type parameter', 422
        sfn = None        
        if 'sfn' in args:
            if args['sfn'] == 'f4a':
                sfn = F4_A()
            elif args['sfn'] == 'e8':
                sfn = E_8()
        return Bracket(bt, sfn).to_json(), 200

if __name__ == 'main':
    app.run()