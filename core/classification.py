#!/F3/core/classification.py
# This module is used for classificating data
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-08

import nltk		# http://www.nltk.org/
import feature_extraction as fe
import tweet_model as tm
import util as util
import random


def train_classifier(dev_tweets, keyword = ""):
	"""Create a classifier that has been trained."""

	random.shuffle(dev_tweets)
	features = fe.create_feature_set(dev_tweets, keyword)
	feature_set = []
	
	for tweet in dev_tweets:
		tweet_features = fe.get_tweet_feature(tweet, features, keyword)
		tweet_sentiment = tweet.sentiment
		feature_set.append((tweet_features, tweet_sentiment))

	
	num_train_set = int (len(feature_set) * 0.6)
	train_set, test_set = feature_set[:num_train_set], feature_set[num_train_set:]
	classifier = nltk.NaiveBayesClassifier.train(train_set)
	
	util.debug("Akurasi : " + str(nltk.classify.accuracy(classifier, test_set))) 
	# print classifier.show_most_informative_features()

	return classifier

def main():
	import __main__
	util.debug(__main__.__file__)
	dev_tweets = tm.get_dev_data()
	train_classifier(dev_tweets, 'sby')

if __name__ == '__main__':
	util.debug('Demi Mei')
	main()