#!/F3/core/tweet_model.py
# A class for representating a tweet.
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-03-30

class tweet_model:
	"""A class for representating a tweet."""
	def __init__(self, id, time, text, sentiment = 0):
		""""Standar __init__ function"""

		self.id = id
		self.time = time
		self.text = text
		self.sentiment = sentiment


	
