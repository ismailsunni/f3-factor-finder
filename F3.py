#!/F3/F3.py
# This module is main module
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-18

import core.classification as classification
import core.factor_finder as ff

class F3:
'''Class defines the program, F3.'''

	def __init__(self, _classifier = None, _factor_finder = None):
		if _classifier == None:
			self._classifier = classification.classifier()
		else:
			self._classifier = _classifier
			
		if _factor_finder == None:
			self._factor_finder = ff.factor_finder([])
		else:
			self._factor_finder = _factor_finder

	# Classifier sector
	def classify_tweets(self, tweets, keyword = "", num_tweet = -1):
		'''Classify list of tweet, return the list of tweet that has been classified.
			And use them to create factor finder.'''
		
		# classify tweets
		tweets = self._classifier.classify_tweets(tweets, keyword, num_tweet)
		
		# create new factor finder
		self._factor_finder = ff.factor_finder(tweets, keyword)
		
		return tweets

