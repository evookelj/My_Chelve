#!/usr/bin/python

from hashlib import sha1
import sqlite3

f = "data/chelve.db"
db = sqlite3.connect(f)
c = db.cursor()

def reg(user, password):
    try: #does table already exist?
        query = ("SELECT * FROM users")
        regOther(user, password);
    except: #if not, first user!
        query = ("CREATE TABLE users (user TEXT, password TEXT, salt TEXT)")
        c.execute(query)
        regFirst(user, password);

def regFirst(user, password):
    print "todo"

def regOther(user, password):
    

register("emma","hi")
db.commit()
db.close()
