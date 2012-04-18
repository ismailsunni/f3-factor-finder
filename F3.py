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
	def train_classifier(self, dev_tweets, train_fraction = 0.5, keyword = ""):
		"""Train classifier using dev_tweets."""

		self._classifier.train_classifier(dev_tweets, train_fraction, keyword)

	def classify(tweet, keyword = ""):
		"""Classify a tweet."""

		return self._classifier.classify(tweet, keyword)

	# Factor Finder sector

