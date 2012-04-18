#!/F3/core/classification.py
# This module is used for classificating data
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-08

import nltk		# http://www.nltk.org/
import feature_extraction as fe
import tweet_model as tm
import util as util
import random


class classifier():
	"""docstring for classifier"""

	def __init__(self, trained = False):
		self.classifier = None
		self.features = None
		self.trained = trained

	def train_classifier(self, dev_tweets, train_fraction = 0.5, keyword = ""):
		"""Train classifier"""

		random.shuffle(dev_tweets)
		features = fe.create_feature_set(dev_tweets, keyword)
		self.features = features
		feature_set = []
		
		for tweet in dev_tweets:
			tweet_features = fe.get_tweet_feature(tweet, features, keyword)
			tweet_sentiment = tweet.sentiment
			feature_set.append((tweet_features, tweet_sentiment))

		num_train_set = int (len(feature_set) * train_fraction)
		train_set = feature_set[:num_train_set]
		
		self.classifier = nltk.NaiveBayesClassifier.train(train_set)

		self.trained = True

	def get_accuracy(self, dev_tweets, train_fraction = 0.5, keyword = ""):
		if self.trained == False:
			return 0
		
		random.shuffle(dev_tweets)
		features = fe.create_feature_set(dev_tweets, keyword)
		self.features = features
		feature_set = []
		
		for tweet in dev_tweets:
			tweet_features = fe.get_tweet_feature(tweet, features, keyword)
			tweet_sentiment = tweet.sentiment
			feature_set.append((tweet_features, tweet_sentiment))
		
		num_train_set = int (len(feature_set) * train_fraction)
		test_set = feature_set[num_train_set:]
		
		return nltk.classify.accuracy(self.classifier, test_set)

	def classify(self, tweet, keyword = ""):
		"""Classify a tweet, r

		Return a sentiment."""
		if self.trained == None:
			util.debug('classifier has not trained yet')
			return None
		else:
			tweet.sentiment =  self.classifier.classify(fe.get_tweet_feature(tweet, self.features, keyword))
			if tweet.negation == True:
				tweet.sentiment *= -1

			return tweet.sentiment

	def classify_tweets(self, tweets, keyword = ""):
		"""Classify list of tweet, return the list of tweet that has been classified."""

		for tweet in tweets:
			self.classify(tweet, keyword)

		return tweets

def main():
	import __main__
	util.debug(__main__.__file__)
	dev_tweets = tm.get_dev_data()
	c = classifier()
	c.train_classifier(dev_tweets, 0.50, 'sby')
	print 'accuracy', c.get_accuracy(dev_tweets, 0.50, 'sby')
	print c.features
	test_data = tm.get_test_data()

	list_sentiment = []
	random.shuffle(test_data)
	retval = c.classify_tweets(test_data[:100], 'sby')
	i = 0
	for r in retval:
		i += 1
		print i, r.text, r.sentiment
		list_sentiment.append(r.sentiment)
	
	print 1, list_sentiment.count(1)
	print 0, list_sentiment.count(0)
	print -1, list_sentiment.count(-1)



if __name__ == '__main__':
	util.debug('Demi Mei')
	main()