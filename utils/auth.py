#!/usr/bin/python

from hashlib import sha1
from sqlite3 import connect
from random import choice

f = "data/chelve.db"
db = connect(f)
c = db.cursor()

def login(user, password):
    count = 0
    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query,(user,));
    for record in sel:
        count += 1
        password = sha1(password+record[1]).hexdigest()
        if (password==record[2]):
            print "User has been logged in"
        else:
            print "User login has failed. Invalid password"
    if count==0:
        print "Username does not exist"

def register(user, password):
    try: #does table already exist?
        c.execute("SELECT * FROM USERS")
    except: #if not, first user!
        query = ("CREATE TABLE users (user TEXT, salt TEXT, password TEXT)")
        c.execute(query)
    regMain(user, password)

def regMain(user, password):
    if regReqs(user, password):
        salt = ''.join([choice('abcdefghijklmnopqrstuvwxyz123456789') for _ in range(10)])
        query = ("INSERT INTO users VALUES (?, ?, ?)");
        password = sha1(password + salt).hexdigest()
        c.execute(query, (user,salt,password));
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
    if " " in user or " " in password:
        print "Spaces not allowed in user or password"
        success = False
    if user==password:
        print "Username and password must be different"
        success = False
    return success

def duplicate(user):
    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query, (user,))
    for record in sel:
        return True
    return False

def getProfile(user):
    userStarted = getStarted(user)
    userContd = getContd(user)

def userStarted(user):
    query = ("SELECT * FROM entries WHERE user=? and number=0")
    sel = c.execute(query, (user,))
    retArr = []
    for record in sel:
        retArr = record[0]
    return retArr

def userContd(user):
    query = ("SELECT * FROM entries WHERE user=? and number>0")
    sel = c.execute(query, (user,))
    retArr = []
    for record in sel:
        retArr = record[0]
    return retArr

register("martians","csTeachers")
login("martians","csTeachers")
db.commit()
db.close()
