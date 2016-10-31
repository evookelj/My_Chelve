#!/usr/bin/python

from hashlib import sha1
import sqlite3

f = "data/chelve.db"
db = sqlite3.connect(f)
c = db.cursor()

def regWrap(user, password):
    try: #does table already exist?
        query = ("SELECT * FROM users")
    except: #if not, first user!
        query = ("CREATE TABLE users (user TEXT, password TEXT, salt TEXT)")
        c.execute(query)
    register(user, password)

def register(user, password):
    if regReqs(user, password):
        query = ("INSERT INTO users VALUES (?, ?, ?)");
        c.execute(query, (user,password,"hi"));
        print "Account created!"

def regReqs(user, password):
    success = True
    if len(password) < 8 or len(password) > 32:
        print "Password must be 8-32 characters"
        success = False
    if len(user) < 8 or len(user) > 32:
        print "Username must be 8-32 characters"
        success = False
    if duplicate(user):
        print "Username already exists"
        success = False
    return success

def duplicate(user):
    query = ("SELECT * FROM users where user=?")
    sel = c.execute(query, (user,))
    for record in sel:
        return True
    return False

register("emaVookelj","hello-there")
db.commit()
db.close()
