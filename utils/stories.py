import sqlite3

<<<<<<< HEAD
# will be used
def getFeed():
	db = sqlite3.connect("data/chelve.db")
	c = db.cursor()
	data = c.execute("SELECT title,timestamp,number FROM entries")
	
	return 0;
	
		
def getUser():
	return 0;

def getProfile():
	return 0;

def getContributors(title):
	return 0;

=======
def getFeed():
    return
		
def getUser():
    return
	
def getContributors(title):
    return
>>>>>>> 43c90d974263d8c31e5ed436821c81e5321ad365

# will be used to print the entire story or most recent contribution
# fullstory vs most recent contribution:
# returns dict with author, timestamp, story

# maybe should take username instead of fullStory and determine permission
# using SEL statements
# ADD an element to dict saying whether they can see full story or not
# so it can return { "story": <story>, "author": author, "timestamp": time, "full": boolean }
def getStory(storyTitle,fullStory):	
	dict = {story:""}
	
	db = sqlite3.connect("data/chelve.db")
	c = db.cursor()
	data = c.execute("SELECT title,number,entry FROM entries")
	
	for x in data:
			if x["title"] == storyTitle:
				dict["author"] = x["user"]
				dict["timestamp"] = x["timestamp"]
				break

	if fullStory:	
		for x in data:
			if x["title"] == storyTitle:
				dict["story"]+= x["entry"]

	else:
		for x in reversed(data):
			if x["title"] == storyTitle:
				dict["story"]+= x["entry"]
				break
	return dict

def getStarted(user):
    query = ("SELECT * FROM entries WHERE user=? and number=0")
    sel = c.execute(query, (user,))
    retArr = []
    for record in sel:
        retArr = record[0]
    return retArr

def getContd(user):
    query = ("SELECT * FROM entries WHERE user=? and number>0")
    sel = c.execute(query, (user,))
    retArr = []
    for record in sel:
        retArr = record[0]
    return retArr

def getProfile(user):
    userStarted = getStarted(user)
    userContd = getContd(user)
    #array of arrays of strs/titles
    return [userStarted, userContd]
		
	
	
	
