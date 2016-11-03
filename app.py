
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

@app.route("/create/<title>")
def createStory(title):

@app.route("/profile/<username>")
def getProfile(username):

#======================#
#         RUN          #
#======================#

if __name__ == "__main__":
    app.debug = True
    app.run() 
