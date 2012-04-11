#!/F3/core/tweet_model.py
# A class for representating a tweet.
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-03-30

from db_control import db_conn

class tweet_model:
	"""A class for representating a tweet."""
	
	def __init__(self, id, time, text, sentiment = 0, negation = 0):
		""""Standar __init__ function"""

		self.id = id
		self.time = time
		self.text = text
		self.negation = negation
		self.sentiment = sentiment


def get_dev_data():
	"""Retrieve data from database for training and test as list of tweet object."""

	db = db_conn()
	tweets = []

	query = "SELECT * FROM " + db.dev_table
	retval = db.read(query)

	for row in retval:
		id = row[0]
		time = row[2]
		text = row[1]
		sentiment = row[3]
		negation = row[4]
		tweets.append(tweet_model(id, time, text, sentiment, negation))

	return tweets

def get_test_data():
	"""Retrieve data from database for training and test as list of tweet object."""

	db = db_conn()
	tweets = []

	query = "SELECT * FROM " + db.test_table
	retval = db.read(query)

	for row in retval:
		id = row[0]
		time = row[2]
		text = row[1]
		sentiment = row[3]
		negation = row[4]
		tweets.append(tweet_model(id, time, text, sentiment, negation))

	return tweets

if __name__ == '__main__':
	pass
