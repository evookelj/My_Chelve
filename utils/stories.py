import sqlite3
import time
import datetime

#returns a list of dictionaries of the 10 most recent stories.
#Each dictionary has keys for title, author, and timestamp.
def getFeed():
    ans = []
    #db = sqlite3.connect("data/chelve.db")
    #c = db.cursor()
    data = c.execute("SELECT title,user,timestamp FROM entries WHERE number=0 LIMIT 10")
    
    #reverse list
    data = data.fetchall()[::-1]
    
    for x in data:
        dict = {}
        dict["title"] = x[0]
        dict["author"] = x[1]
        dict["timestamp"] = x[2]
        ans.append(dict)
        
    return ans
    
#returns list of contributors to a given story
def getContributors(storyTitle):
    contributors = []
    # db = sqlite3.connect("data/chelve.db")
    # c = db.cursor()
    data = c.execute("SELECT user FROM entries WHERE title=?",(storyTitle,))
    for x in data:
        contributors.append(x[0])
    return contributors

# will be used to print the entire story or most recent contribution
# fullstory vs most recent contribution:
# returns dict with author, timestamp, story

# ADD an element to dict saying whether they can see full story or not
# so it can return { "story": <story>, "author": author, "timestamp": time, "full": boolean }
def getStory(storyTitle,username):  
    dict = {"story":""}
    # db = sqlite3.connect("data/chelve.db")
    # c = db.cursor()
    data = c.execute("SELECT * FROM entries WHERE title=?",(storyTitle,))
    data = data.fetchall()
    print ("------")
    print(data)
    print ("------")
    dict["author"] = data[0][4]
    dict["timestamp"] = data[0][1]
    
    #gets user contributiion to story if it exists
    data2 = c.execute("SELECT title, user FROM entries WHERE title=? AND user=?",(storyTitle,username))
    
    #if user contribution exists
    if data2.fetchall():
        dict["full"] = True
        for x in data:
            dict["story"] += x[3]
    else:
        dict["full"] = False
        dict["story"] += data[-1][3] 
    return dict
    
def getStarted(user):
    # db = sqlite3.connect("data/chelve.db")
    # c = db.cursor()
    query = ("SELECT * FROM entries WHERE user=? and number=0")
    sel = c.execute(query, (user,))
    retArr = []
    for record in sel:
        retArr.append(record[0])
    return retArr

def getContd(user):
    # db = sqlite3.connect("data/chelve.db")
    # c = db.cursor()
    query = ("SELECT * FROM entries WHERE user=? and number>0")
    sel = c.execute(query, (user,))
    retArr = []
    for record in sel:
        retArr.append(record[0])
    return retArr

def getProfile(user):
    userStarted = getStarted(user)
    userContd = getContd(user)
    #array of arrays of strs/titles
    return [userStarted, userContd]
            
#should work for starting a story as well as contributing to a story
#timestamp will be a string in 
def contributeTo(storyTitle,entry,user):
    # db = sqlite3.connect("data/chelve.db")
    # c = db.cursor()
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S %Y-%m-%d')
    query = ("SELECT * FROM entries WHERE title=? AND number=(SELECT MAX(number) FROM entries WHERE title=?)")
    data = c.execute(query,(storyTitle,storyTitle))
    try:
        number=data.fetchone()[2] + 1
    except:
        number=0
    query = ("INSERT INTO entries VALUES (?,?,?,?,?)")
    c.execute(query,(storyTitle,timestamp,number,entry,user,))
    db.commit()
    db.close()
    
#import os
#os.chdir("..")
db = sqlite3.connect("data/chelve.db")
c = db.cursor()



