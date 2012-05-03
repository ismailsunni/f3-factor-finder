#!/F3/core/classification.py
# This module is used for classificating data
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-08

from __future__ import division
import time
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

	def train_classifier(self, dev_tweets, num_tweet = -1, keyword = "", dict_param = None, min_occur = 1):
		"""Train classifier"""

		random.shuffle(dev_tweets)
		if not (num_tweet <= -1 or num_tweet > len(dev_tweets)):
			dev_tweets = dev_tweets[:num_tweet]

		features = fe.create_feature_set(dev_tweets, keyword, min_occur, dict_param)
		self.features = features
		feature_set = []
		
		i = 0
		for tweet in dev_tweets:
			i += 1
			if i % 100 == 0:
				print i
			tweet_features = fe.get_tweet_feature(tweet, features, keyword, dict_param)
			tweet_sentiment = tweet.sentiment
			feature_set.append((tweet_features, tweet_sentiment))

		train_set = feature_set
		
		self.classifier = nltk.NaiveBayesClassifier.train(train_set)
		self.trained = True

	def get_accuracy_cross_validation(self, dev_tweets, num_tweet = -1, fold = 10, keyword = "", random_seed = 0, min_occur = 1, dict_param = None):
		"""Return accuracy by using cross validation method."""

		list_accuracy = []
		last = 0.0
		t0 = time.clock()
		
		# num_tweet
		if not (num_tweet <= -1 or num_tweet > len(dev_tweets)):
			dev_tweets = dev_tweets[:num_tweet]

		random.seed(random_seed)
		random.shuffle(dev_tweets)

		avg = len(dev_tweets) / fold
		p = 0
		while last < len(dev_tweets) - 1:
			print p
			p += 1
			train_tweet = dev_tweets[:int(last)] + dev_tweets[int(last+avg):]
			test_tweet = dev_tweets[int(last):int(last+avg)]

			features = fe.create_feature_set(train_tweet, keyword, min_occur, dict_param)

			feature_set = []
			for tweet in train_tweet:
				tweet_features = fe.get_tweet_feature(tweet, features, keyword, dict_param)
				tweet_sentiment = tweet.sentiment
				feature_set.append((tweet_features, tweet_sentiment))
			test_feature_set = []
			for tweet in test_tweet:
				tweet_features = fe.get_tweet_feature(tweet, features, keyword, dict_param)
				tweet_sentiment = tweet.sentiment
				test_feature_set.append((tweet_features, tweet_sentiment))

			self.classifier = nltk.NaiveBayesClassifier.train(feature_set)
			list_accuracy.append(nltk.classify.accuracy(self.classifier, test_feature_set))
			last += avg

		t1 = time.clock()

		print 'while time: ', t1-t0
		sum_accuracy = 0.0
		for accuracy in list_accuracy[:fold]:
			sum_accuracy += accuracy
		print list_accuracy
		print sum_accuracy, len(list_accuracy)
		return sum_accuracy / fold

	def classify(self, tweet, keyword = "", dict_param = None):
		"""Classify a tweet, r

		Return a sentiment."""
		if self.trained == None:
			util.debug('classifier has not trained yet')
			return None
		else:
			tweet.sentiment =  self.classifier.classify(fe.get_tweet_feature(tweet, self.features, keyword, dict_param))
			if tweet.negation == True:
				tweet.sentiment *= -1

			return tweet.sentiment

	def classify_tweets(self, tweets, keyword = "", dict_param = None, num_tweet = -1):
		"""Classify list of tweet, return the list of tweet that has been classified."""

		if not (num_tweet <= -1 or num_tweet > len(tweets)):
			tweets = tweets[:num_tweet]

		i = 0
		for tweet in tweets:
			i += 1
			if i % 100 == 0:
				print i
			self.classify(tweet, keyword, dict_param)

		return tweets

def main():
	start_time = time.asctime()
	print start_time


	import __main__
	util.debug(__main__.__file__)
	t1 = time.clock()
	dev_tweets = tm.get_dev_data()

	t2 = time.clock()
	print "get dev data : ", t2 - t1
	c = classifier()
	print 'akurasi : ', c.get_accuracy_cross_validation(dev_tweets)
	t3 = time.clock()
	print 'create classifier : ', t3 - t2
	c.train_classifier(dev_tweets)
	t4 = time.clock()
	print "train time : ", t4 - t3
	test_data = tm.get_test_data('dahlan iskan')
	t5 = time.clock()
	print 'get test_data : ', t5-t4

	list_sentiment = []
	random.shuffle(test_data)
	retval = c.classify_tweets(test_data[:1000], 'dahlan iskan')
	i = 0
	for r in retval:
		i += 1
		r.print_tweet()
		list_sentiment.append(r.sentiment)
	t6 = time.clock()
	print 'classify 1000 tweet : ', t6-t5
	print 1, list_sentiment.count(1)
	print 0, list_sentiment.count(0)
	print -1, list_sentiment.count(-1)

	end_time = time.asctime()
	print "end_time", end_time

if __name__ == '__main__':
	util.debug('Demi Mei')
	main()