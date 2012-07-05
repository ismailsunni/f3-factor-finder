#!/F3/core/feature_extraction.py
# This module is used for extracting feature
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-08

import util as util
import preprocess as pp
import tweet_model as tm

debug_fe = 1

def extract_feature(tweet, keyword = "", dict_param = None):
	'''Extracting feature from a tweet.'''
	# print 'alpha', dict_param
	if not tweet.parsed:
		# print 'fe, line 15 not parsed'
		tweet.preprocess(dict_param)
	features = util.remove_all_values_from_list(tweet.parsed_word, keyword)
	# print 'fe, line 18', features
	return features

def create_feature_set(dev_tweets, keyword = "", min_occur = 1, dict_param = None):
	'''Create set of feature that will be used to train classifier.'''

	features = set()
	feature_list = []

	for tweet in dev_tweets:
		new_feature = set(extract_feature(tweet, keyword, dict_param))
		feature_list.extend(new_feature)
		features |= new_feature

	retval = []
	for feature in features:
		if feature_list.count(feature) > min_occur:
			retval.append(feature)

	# return features
	
	return retval

def get_tweet_feature(tweet, features, keyword = "", dict_param = None, max_distance = 1):
	'''Get features of a tweet.'''
	
	tweet_features = {}
	tweet_raw_features = extract_feature(tweet, keyword, dict_param)

	for feature in features:
		# tweet_features[feature] = tweet_raw_features.count(feature)	# count
		tweet_features[feature] =  feature in tweet_raw_features #or pp.is_near_words(feature, tweet_raw_features, max_distance)

	return tweet_features