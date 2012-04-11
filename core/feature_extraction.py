#!/F3/core/feature_extraction.py
# This module is used for extracting feature
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-08

import util as util
import preprocess as pp
import tweet_model as tm

debug_fe = 1

def extract_feature(tweet, keyword):
	"""Extracting feature from a tweet."""

	return extract_unigram(tweet, keyword)

def extract_unigram(tweet, keyword):
	"""Extracting feature from a tweet by unigram."""

	tweet.negation, features = pp.preprocess_tweet(tweet.text)
	
	features = features.split(' ')
	features = util.remove_all_values_from_list(features, keyword)

	# print tweet.texts
	# print features
	return features

def create_feature_set(dev_tweets, keyword = ""):
	"""Create set of feature that will be used to train classifier."""

	features = set()
	for tweet in dev_tweets:
		new_feature = set(extract_feature(tweet, keyword))
		features |= new_feature

	util.debug(features, debug_fe)
	# print 'features', features
	return features

def get_tweet_feature(tweet, features, keyword = ""):
	"""Get features of a tweet."""

	tweet_features = {}
	tweet_raw_features = extract_feature(tweet, keyword)

	for feature in features:
		tweet_features[feature] = tweet_raw_features.count(feature)	# count
		# tweet_features[feature] =  feature in tweet_raw_features

	print tweet.text
	print tweet_features
	return tweet_features