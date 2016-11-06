#!/usr/bin/python

from hashlib import sha1
from sqlite3 import connect
from os import urandom

f = "data/chelve.db"#might have to be moved to individual methods (IDK)
db = connect(f)
c = db.cursor()

def login(user, password):
    
    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query,(user,));
    
    #records with this username
    #so should be at most one record (in theory)
     
    for record in sel:
        password = sha1(password+record[1]).hexdigest()##record[1] is the salt
        if (password==record[2]):
            return ""#no error message because it will be rerouted to mainpage
        else:
            return "User login has failed. Invalid password"#error message
    return "Username does not exist"#error message

def register(user, password):
    try: #does table already exist?
        c.execute("SELECT * FROM USERS")
    except: #if not, this is the first user!
        c.execute("CREATE TABLE users (user TEXT, salt TEXT, password TEXT)")
    return regMain(user, password)#register helper

def regMain(user, password):#register helper
    reg = regReqs(user, password)
    if reg == "":
        salt = os.urandom(10)
        query = ("INSERT INTO users VALUES (?, ?, ?)")
        password = sha1(password + salt).hexdigest()
        c.execute(query, (user, salt, password))
        return "Account created!"
    return reg
        
def regReqs(user, password):
    if len(password) < 8 or len(password) > 32:
        return "Password must be 8-32 characters"#this is something we want the user to be able to see
    if len(user) < 8 or len(user) > 32:
        return "Username must be 8-32 characters"
    if duplicate(user):
        return "Username already exists"
    if " " in user or " " in password:
        return "Spaces not allowed in user or password"
    if user==password:
        return "Username and password must be different"
    return ""

def duplicate(user):
    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query, (user,))
    for record in sel:
        return True
    return False

db.commit()
db.close()
