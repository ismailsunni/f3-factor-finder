#!/F3/core/feature_extraction.py
# This module is used for extracting feature
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-08

import util as util

def extract_feature(tweet, keyword):
	"""Extracting feature from a tweet."""

	return extract_unigram(tweet, keyword)

def extract_unigram(tweet, keyword):
	"""Extracting feature from a tweet by unigram."""

	features = tweet.split(' ')
	util.remove_all_values_from_list(features, keyword)

	return features

