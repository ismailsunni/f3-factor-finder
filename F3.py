#!/F3/F3.py
# This module is main module
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-18

import core.classification as classification
import core.factor_finder as ff

class F3:
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
	def train_classifier(self, dev_tweets, num_tweet = -1, keyword = "", dict_param = None, min_occur = 1):
		"""Train classifier using dev_tweets."""

		self._classifier.train_classifier(dev_tweets, num_tweet, keyword, dict_param, min_occur)

	def classify(self, tweet, keyword = "", dict_param = None):
		"""Classify a tweet."""

		return self._classifier.classify(tweet, keyword, dict_param = None)

	def classify_tweets(self, tweets, keyword = "", dict_param = None, num_tweet = -1):
		"""Classify list of tweet, return the list of tweet that has been classified."""

		if not (num_tweet <= -1 or num_tweet > len(tweets)):
			tweets = tweets[:num_tweet]
			print len(tweets)

		for tweet in tweets:
			self.classify(tweet, keyword, dict_param)

		return tweets

	def get_accuracy_cross_validation(self, dev_tweets, num_tweet = -1, fold = 10, keyword = "", random_seed = 0, min_occur = 1, dict_param = None):

		return self._classifier.get_accuracy_cross_validation(dev_tweets, num_tweet, fold, keyword, random_seed, min_occur, dict_param)

	# Factor Finder sector

