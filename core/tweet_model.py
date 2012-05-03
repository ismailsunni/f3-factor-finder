#!/F3/core/tweet_model.py
# A class for representating a tweet.
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-03-30

from db_control import db_conn
from datetime import datetime
import preprocess as pp

class tweet_model:
	"""A class for representating a tweet."""
	
	def __init__(self, id, time, text, sentiment = 0, negation = 0):
		""""Standar __init__ function"""

		self.id = id
		self.time = time
		self.text = text
		self.negation = negation
		self.sentiment = sentiment
		self.parsed_word = []
		self.parsed = False

	def print_tweet(self):
		"""Print procedure"""
		import unicodedata
		print unicodedata.normalize('NFKD', self.text.decode('latin-1')).encode('ascii', 'ignore'), self.sentiment

	def get_normal_text(self):

		import unicodedata
		return unicodedata.normalize('NFKD', self.text.decode('latin-1')).encode('ascii', 'ignore')

	def preprocess(self, dict_param = None):
		"""Preprocess a tweet and save the result in parsed_word and negation."""
		
		self.negation, preprocesssed_text = pp.preprocess_tweet(self.text, dict_param)
		self.parsed_word = preprocesssed_text.split(' ')
		self.parsed = True

def get_dev_data():
	"""Retrieve data from database for training and test as list of tweet object."""

	db = db_conn()
	tweets = []

	query = "SELECT * FROM " + db.test_table + " WHERE `dev_tweet` = 1"
	retval = db.read(query)

	for row in retval:
		id = row[0]
		time = row[2]
		text = row[1]
		sentiment = row[3]
		negation = row[4]
		tweets.append(tweet_model(id, time, text, sentiment, negation))

	return tweets

def get_test_data(keyword = "", start_time = None, end_time = None):
	"""Retrieve data from database for training and test as list of tweet object."""

	db = db_conn()
	tweets = []

	query = "SELECT * FROM " + db.test_table
	where = " WHERE `tweet_text` LIKE '%" + keyword + "%' AND `dev_tweet` != 1"
	if start_time != None:
		where += " AND `created_at` >= '" + start_time.__str__() + "'"
	if end_time != None:
		where += " AND `created_at` <= '" + end_time.__str__() + "'"

	retval = db.read(query + where)
	# print query + where

	for row in retval:
		id = row[0]
		time = row[2]
		text = row[1]
		sentiment = row[3]
		negation = row[4]
		tweets.append(tweet_model(id, time, text, sentiment, negation))

	return tweets

if __name__ == '__main__':
	t = get_test_data('dear', datetime(2012, 3, 4, 0, 0, 0), datetime(2012, 3, 5, 0, 0, 0))
	for s in t:
		print s.time, s.text
