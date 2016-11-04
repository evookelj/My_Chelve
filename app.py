
#======================#
#        SETUP         #
#======================#

from flask import Flask, render_template, request, session, redirect, url_for
import os
from utils import auth, stories

app = Flask(__name__)
app.secret_key = os.urandom(24)

#======================#
#    METHODS/ROUTES    #
#======================#

@app.route("/")
def homePage():
    if not "Username" in session:
        return redirect(url_for('login'))
    return render_template('homepage.html', username = session["Username"])
##needs implementation of feed

@app.route("/login")
def login():
    if "Username" in session:
        return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route("/authenticate")
def auth():
    pw = request.form["pass"]
    un = request.form["user"]
    
    if request.form["name"] == "register":
        return render_template('login.html', result = auth.register(un, pw))
        
    if request.form["name"] == "login":
        text = auth.login()
        if text == "":
            return redirect(url_for('homepage'))
        return render_template('login.html', result = text)
    
        
@app.route("/story/<title>")
def getStory(title):
    

@app.route("/create")
def createStory():
    

@app.route("/profile/<user>")
def getProfile(user):
    duple = getProfile(user);
    return render_template('profile.html',
                            username = user,
                            startedStories = duple[0],
                            addStories = duple[1])

#======================#
#         RUN          #
#======================#

if __name__ == "__main__":
    app.debug = True
    app.run() 
