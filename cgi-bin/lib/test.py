#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import lxml.html
import MySQLdb

TABLE = "bracketo_marchmadness"

def connect():
    return MySQLdb.connect(host="engr-cpanel-mysql.engr.illinois.edu",
                           user="bracketo_client",
                           passwd="M@rchM@dn355",
                           db="bracketo_marchmadness")

def main():
    print "Testing connection..."
    db = connect()
    cur = db.cursor()
    try:
        cur.execute("""SELECT * FROM Bracket""")
        print cur.fetchone()
    except MySQLdb.Error as e:
        raise e
    finally:
        cur.close()
        db.close()

if __name__ == "__main__":
    main()

