import sqlite3


def getFeed():
	
	
		
def getUser():
	
	
	
	
def getProfile():
	

	
def getContributors(title):
	


# will be used to print the entire story or most recent contribution
# fullstory vs most recent contribution:
def getStory(storyTitle,fullStory):	
	# returns dict with author, timestamp, story 
	dict = {story:""}
	
	db = sqlite3.connect("data/chelve.db")
	c = db.cursor()
	data = c.execute("SELECT title,number,entry FROM entries")
	
	
	if fullStory:
		for x in data:
			
			if x[title] == storyTitle:
				story+= x[entry]
			
				
	else:
		for x in data:
			
		
	
	
	
