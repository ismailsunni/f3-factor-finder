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

	def train_classifier(self, dev_tweets, train_fraction = 1, keyword = ""):
		"""Train classifier"""

		random.shuffle(dev_tweets)
		features = fe.create_feature_set(dev_tweets, keyword)
		self.features = features
		feature_set = []
		
		for tweet in dev_tweets:
			tweet_features = fe.get_tweet_feature(tweet, features, keyword)
			tweet_sentiment = tweet.sentiment
			feature_set.append((tweet_features, tweet_sentiment))

		# num_train_set = int (len(feature_set) * train_fraction)
		train_set = feature_set
		# test_set = feature_set[num_train_set:]
		
		self.classifier = nltk.NaiveBayesClassifier.train(train_set)

		# print 'akurasi : ', nltk.classify.accuracy(self.classifier, test_set)

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

	def get_accuracy_cross_validation(self, dev_tweets, fold = 10, keyword = ""):
		"""Return accuracy by using cross validation method."""
		list_accuracy = []
		last = 0.0

		# random.seed(8)
		# random.shuffle(dev_tweets)
		# features = fe.create_feature_set(dev_tweets, keyword)
		# self.features = features
		
		# feature_set = []
		# for tweet in dev_tweets:
		# 	tweet_features = fe.get_tweet_feature(tweet, features, keyword)
		# 	tweet_sentiment = tweet.sentiment
		# 	feature_set.append((tweet_features, tweet_sentiment))
		# print feature_set
		t0 = time.clock()
		avg = len(dev_tweets) / fold
		while last < len(dev_tweets) - 1:
			train_tweet = dev_tweets[:int(last)] + dev_tweets[int(last+avg):]
			test_tweet = dev_tweets[int(last):int(last+avg)]

			features = fe.create_feature_set(train_tweet, keyword, 3)
			# print features

			feature_set = []
			for tweet in train_tweet:
				tweet_features = fe.get_tweet_feature(tweet, features, keyword)
				tweet_sentiment = tweet.sentiment
				feature_set.append((tweet_features, tweet_sentiment))
			# util.print_index_list_dict(feature_set)
			test_feature_set = []
			for tweet in test_tweet:
				tweet_features = fe.get_tweet_feature(tweet, features, keyword)
				tweet_sentiment = tweet.sentiment
				test_feature_set.append((tweet_features, tweet_sentiment))

			# train_set = feature_set[0:int(last)] + feature_set[int(last+avg):]
			# test_set = feature_set[int(last):int(last+avg)]
			self.classifier = nltk.NaiveBayesClassifier.train(feature_set)
			# print self.classifier.most_informative_features(100)
			list_accuracy.append(nltk.classify.accuracy(self.classifier, test_feature_set))
			last += avg
		t1 = time.clock()

		print 'while time: ', t1-t0
		sum_accuracy = 0.0
		for accuracy in list_accuracy:
			sum_accuracy += accuracy
		print list_accuracy
		print sum_accuracy, len(list_accuracy)
		return sum_accuracy / len(list_accuracy)


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
	a = time.asctime()
	print a
	t0 = time.clock()
	dev_tweets = tm.get_dev_data()
	t1 = time.clock()
	c = classifier()
	t2 = time.clock()
	print c.get_accuracy_cross_validation(dev_tweets, 10, '')
	t3 = time.clock()
	
	b = time.asctime()
	print b
	# print 'delta : ', b - a
	print 'time get data : ', t1-t0
	print 'classifier : ', t2-t1
	print 'cross : ', t3-t2
	print 'total : ', time.clock()

	# print c.features
	test_data = tm.get_test_data('dahlan iskan')
	c.train_classifier(dev_tweets)

	list_sentiment = []
	random.shuffle(test_data)
	retval = c.classify_tweets(test_data[:100], 'dahlan iskan')
	i = 0
	for r in retval:
		i += 1
		r.print_tweet()
		list_sentiment.append(r.sentiment)
	
	print 1, list_sentiment.count(1)
	print 0, list_sentiment.count(0)
	print -1, list_sentiment.count(-1)



if __name__ == '__main__':
	util.debug('Demi Mei')
	main()