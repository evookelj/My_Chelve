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
        #if the user is not logged in
        #then homepage has nothing for them so redirects to login
        return redirect(url_for('login'))
    return render_template('homepage.html', username = session["Username"],feed=stories.getFeed())

@app.route("/login/")
def login():
    if "Username" in session:
        return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route("/authenticate/", methods=['POST'])
def authenticate():
    pw = request.form["pass"]
    un = request.form["user"]
    tp = request.form["action"]#login vs. register
    
    if tp == "register":
        regRet = auth.register(un,pw)#returns an error/success message
        return render_template('login.html', result = regRet)
        
    if tp == "login":
        text = auth.login(un,pw)#error message
        if text == "":#if no error message, succesful go back home
            session["Username"] = un
            return redirect(url_for('homePage'))
        return render_template('login.html', result = text)
    
        
@app.route("/story/<title>/")
def getStory(title):
    story = stories.getStory(title, session["Username"])#needs username to decide how much permission the user has
    
    if story["full"]:#user has already contributed so has full viewing permissions
        return render_template("cStory.html",
                               story = story["story"],
                               author = story["author"],
                               time = story["timestamp"],
                               username=session["Username"]);
    
    return render_template("ncStory.html", #otherwise, user has not contributed and can only see most recent addition
                           story=story["story"],
                           author=story["author"],
                           time=story["timestamp"])

@app.route("/create/")
def createStory(): #where user creates a new story or contributed to an existing one
    return render_template("createStory.html")

@app.route("/created/", methods=['POST']) #intermediary for /create
def created():
    title = request.form["title"]
    entry = request.form["story"]
    user = session["Username"]
    stories.contributeTo(title, entry, user)
    return redirect( url_for('homePage'))

@app.route("/profile/")
def getMyProfile():#goes to user who's logged in's profile
    return getProfile(session["Username"])

@app.route("/profile/<user>/")
def getProfile(user):
    duple = stories.getProfile(user);#duple has started stories, as well as stories contributed to
    return render_template('profile.html',
                            username = user,
                            startedstories = duple[0],
                            addstories = duple[1])

@app.route("/logout/")
def logOut():
    if "Username" in session:# can only log out if you are already logged in
        session.pop("Username")
    return redirect (url_for('homePage'))

#======================#
#         RUN          #
#======================#

if __name__ == "__main__":
    app.debug = True
    app.run() 
