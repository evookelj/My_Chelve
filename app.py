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

@app.route("/login/")
def login():
    if "Username" in session:
        return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route("/authenticate/", methods=['POST'])
def authenticate():
    pw = request.form["pass"]
    un = request.form["user"]
    tp = request.form["action"]
    if tp == "register":
        regRet = auth.register(un,pw)
        return render_template('login.html', result = regRet)
        
    if tp == "login":
        text = auth.login(un,pw)
        if text == "":
            session["Username"] = un
            return redirect(url_for('homePage'))
        return render_template('login.html', result = text)
    
        
@app.route("/story/<title>/")
def getStory(title):
    story = stories.getStory(title, session["Username"])
    if story["full"]:
        return render_template("cStory.html", story = story["story"], author = story["author"], time = story["timestamp"]);
    return render_template("ncStory.html", story=story["story"], author=story["author"], time=story["timestamp"])

@app.route("/create/")
def createStory():
    return render_template("createStory.html")

@app.route("/created/", methods=['POST']) #intermediary for /create
def created():
    title = request.form["title"]
    entry = request.form["story"]
    user = session["Username"]
    stories.contributeTo(title, entry, user)
    return redirect( url_for('homePage'))

@app.route("/profile/")
def getMyProfile():
    return redirect( url_for("getProfile", user=session["Username"]))

@app.route("/profile/<user>/")
def getProfile(user):
    duple = stories.getProfile(user);
    return render_template('profile.html',
                            username = user,
                            startedstories = duple[0],
                            addstories = duple[1])

#======================#
#         RUN          #
#======================#

if __name__ == "__main__":
    app.debug = True
    app.run() 
