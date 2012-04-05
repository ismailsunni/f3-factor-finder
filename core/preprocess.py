#!/F3/core/preprocess.py
# This file is used for preprocessing
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-03-30

import re
import util as util
import ttp	# module from https://github.com/BonsaiDen/twitter-text-python

#	Global variables
negation_words_file = "negation_words.txt"	# Created by ismailsunni
stop_words_file = "stop_words.txt"			# Downloaded from http://fpmipa.upi.edu/staff/yudi/stop_words_list.txt and added by ismailsunni


def fold_case(tweet):
	'''Fold case of a string.'''
	
	return tweet.lower()
	
def remove_RT(tweet):
	'''Obvious function.'''

	return tweet.replace(' RT ', ' ')

def remove_username(tweet):
	'''Obvious function.'''

	p = ttp.Parser()
	users = p.parse(tweet).users
	for user in users:
		tweet = tweet.replace('@'+user, '')

	return tweet

def remove_URL(tweet):
	'''Obvious function.'''	

	p = ttp.Parser()
	urls = p.parse(tweet).urls
	for url in urls:
		tweet = tweet.replace(url, '')

	return tweet

def remove_hashtag(tweet):
	'''Obvious function.'''	

	p = ttp.Parser()
	tags = p.parse(tweet).tags
	for tag in tags:
		tweet = tweet.replace('#'+tag, '')

	return tweet

def clean_number(tweet):
	'''Clean number from tweet. Number which is cleaned is stand-alone, begining of word, and end of word number.'''

	regex_begin = r'(\A| )\d+'
	regex_end = r'\d+( |\Z|\z)'
	regex_space = r'\s{2,}'

	tweet = re.sub(regex_begin, ' ', tweet)
	tweet = re.sub(regex_end, ' ', tweet)
	tweet = re.sub(regex_space, ' ', tweet)

	return tweet

def clean_one_char(tweet):
	'''Clean a character surround by whitespace.'''

	regex_one_char = r'\s\S\s'

	tweet = re.sub(regex_one_char, ' ', tweet)

	return tweet

def convert_number(tweet):
	'''Convert number to certain character.'''

	tweet = tweet.replace('00', 'u')
	tweet = tweet.replace('0', 'o')
	tweet = tweet.replace('1', 'i')
	tweet = tweet.replace('3', 'e')
	tweet = tweet.replace('4', 'a')
	tweet = tweet.replace('5', 's')
	tweet = tweet.replace('6', 'g')
	tweet = tweet.replace('7', 't')
	tweet = tweet.replace('8', 'b')
	tweet = tweet.replace('9', 'g')

	new_tweet = []

	for i in xrange(0,len(tweet)):
		if tweet[i] != '2':
			new_tweet.append(tweet[i])
		else:
			new_tweet.append(tweet[i-1])

	return ''.join(new_tweet)

def convert_negation(tweet):
	'''Count negation word. If odd, it is a negation tweet, return True, otherwise not.'''
	
	negation_words = util.read_text_file(negation_words_file)
	num_negation_word = 0
	new_tweet = []
	tweet_words = tweet.split(' ')

	for tweet_word in tweet_words:
		if tweet_word in negation_words:
			num_negation_word += 1
		else:
			new_tweet.append(tweet_word)
	
	if num_negation_word % 2 == 1:
		return {'negation':True, 'tweet':' '.join(new_tweet)}
	else:
		return {'negation':False, 'tweet':' '.join(new_tweet)}

def remove_stop_words(tweet):
	'''Remove stop words.'''

	stop_words = util.read_text_file(negation_words_file)
	tweet_words = tweet.split(' ')
	new_tweet = []

	for tweet_word in tweet_words:
		if tweet_word not in stop_words:
			new_tweet.append(tweet_word)

	return ' '.join(new_tweet)

def convert_emoticon(tweet):
	'''Convert emoticon to corresponding term.'''
	# To do
	# load from yaml, get dictionary
	# Replace all
	pass



if __name__ == '__main__':
	string = 'Assalamu\'alaikum wrwb. Pagi rekan2. Kadang hati lbh hidup saat ingat kematian. Saat kebohongan tak lg diperlukan. Berkah, sehat & Semangat!'
	print remove_URL(string)
	print remove_hashtag(string)
	print remove_username(string)
	print clean_number(string)
	print convert_number(string)
	print convert_negation(string)
	print remove_stop_words(string)