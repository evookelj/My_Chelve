
#======================#
#        SETUP         #
#======================#

from flask import Flask, render_template, request, session, redirect, url_for
import os
from utils import auth, stories

app = Flask(__name__))
app.secret_key = os.urandom(24)

#======================#
#    METHODS/ROUTES    #
#======================#

@app.route("/")
def homePage():

@app.route("/login")
def login():

@app.route("/authenticate")
def auth():

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
