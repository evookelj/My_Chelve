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
            return ""
        else:
            return "User login has failed. Invalid password" #debugging purposes, to be removed in final
    if count==0:
        return "Username does not exist" #debugging purposes, to be removed in final

def register(user, password):
    try: #does table already exist?
        c.execute("SELECT * FROM USERS")
    except: #if not, first user!
        query = ("CREATE TABLE users (user TEXT, salt TEXT, password TEXT)")
        #doesn't actually affect functionality or efficiency, but why create a variable (query) that is only gonna be used once?
        #why not:
        #c.execute("CREATE TABLE users (user TEXT, salt TEXT, password TEXT)")
        c.execute(query)
    return regMain(user, password)

def regMain(user, password):
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


register("martians","csTeachers")
login("martians","csTeachers")
db.commit()
db.close()
