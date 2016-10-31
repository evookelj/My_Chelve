#!/usr/bin/python

from hashlib import sha1
import sqlite3

f = "data/chelve.db"
db = sqlite3.connect(f)
c = db.cursor()

salt = "hi"

def login(user, password):
    count = 0
    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query,(user,));
    for record in sel:
        count += 1
        password = sha1(password+salt).hexdigest()
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
        query = ("INSERT INTO users VALUES (?, ?, ?)");
        password = sha1(password + salt).hexdigest()
        c.execute(query, (user,"hi",password));
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
    query = ("SELECT * FROM users where user=?")
    sel = c.execute(query, (user,))
    for record in sel:
        return True
    return False

register("martians","csTeachers")
login("martians","sesameStreet")
db.commit()
db.close()
