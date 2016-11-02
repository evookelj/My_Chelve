#!/usr/bin/python

from hashlib import sha1
from sqlite3 import connect
from os import urandom

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
            print "User has been logged in" #debugging purposes, to be removed in final
            return True
        else:
            print "User login has failed. Invalid password" #debugging purposes, to be removed in final
            return False
    if count==0:
        print "Username does not exist" #debugging purposes, to be removed in final
        return False

def register(user, password):
    try: #does table already exist?
        c.execute("SELECT * FROM USERS")
    except: #if not, first user!
        query = ("CREATE TABLE users (user TEXT, salt TEXT, password TEXT)")
        #doesn't actually affect functionality or efficiency, but why create a variable (query) that is only gonna be used once?
        #why not:
        #c.execute("CREATE TABLE users (user TEXT, salt TEXT, password TEXT)")
        c.execute(query)
    regMain(user, password)

def regMain(user, password):
    reg = regReqs(user, password)
    if reg:
        salt = os.urandom(10)
        query = ("INSERT INTO users VALUES (?, ?, ?)")
        password = sha1(password + salt).hexdigest()
        c.execute(query, (user, salt, password))
        print "Account created!"
    return reg
        
def regReqs(user, password):
    success = True
    if len(password) < 8 or len(password) > 32:
        print "Password must be 8-32 characters"#this is something we want the user to be able to see
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

def getProfile(user):#move to stories.py
    userStarted = getStarted(user)
    userContd = getContd(user)
    return [userStarted, userContd]

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
