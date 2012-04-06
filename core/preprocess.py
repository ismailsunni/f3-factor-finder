#!/F3/core/preprocess.py
# This file is used for preprocessing
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-03-30

import re
import unicodedata
import util as util
import ttp	# module from https://github.com/BonsaiDen/twitter-text-python

#	Global variables
negation_words_file = "negation_words.txt"	# Created by ismailsunni
stop_words_file = "stop_words.txt"			# Downloaded from http://fpmipa.upi.edu/staff/yudi/stop_words_list.txt and added by ismailsunni
emoticons_file = "emoticons.yaml"

def normalize_character(tweet):
    """Normalize a string from unicode character."""

    return unicodedata.normalize('NFKD', tweet.decode('latin-1')).encode('ascii', 'ignore')

def fold_case(tweet):
	"""Fold case of a string."""
	
	return tweet.lower()
	
def remove_RT(tweet):
	"""Obvious function."""

	regex_RT = r'\s(RT|rt)\s'
	tweet = re.sub(regex_RT, ' ', tweet)
	
	return tweet

def remove_username(tweet):
	"""Obvious function."""

	p = ttp.Parser()
	users = p.parse(tweet).users
	for user in users:
		tweet = tweet.replace('@'+user, '')

	return tweet

def remove_URL(tweet):
	"""Obvious function."""	

	p = ttp.Parser()
	urls = p.parse(tweet).urls
	for url in urls:
		tweet = tweet.replace(url, '')

	return tweet

def remove_hashtag(tweet):
	"""Obvious function."""	

	p = ttp.Parser()
	tags = p.parse(tweet).tags
	for tag in tags:
		tweet = tweet.replace('#'+tag, '')

	return tweet

def clean_number(tweet):
	"""Clean number from tweet. Number which is cleaned is stand-alone, begining of word, and end of word number."""

	regex_begin = r'(\A| )\d+'
	regex_end = r'\d+( |\Z|\z)'
	regex_space = r'\s{2,}'

	tweet = re.sub(regex_begin, ' ', tweet)
	tweet = re.sub(regex_end, ' ', tweet)
	tweet = re.sub(regex_space, ' ', tweet)

	return tweet

def clean_one_char(tweet):
	"""Clean a character surround by whitespace."""

	# bug found
	# regex_one_char = r'\s+\S\s+'

	# tweet = re.sub(regex_one_char, ' ', tweet)

	words = tweet.split(' ')
	words_temp = []

	for word in words:
		if len(word) > 1:
			words_temp.append(word)

	tweet = ' '.join(words_temp)

	return tweet

def convert_number(tweet):
	"""Convert number to certain character."""

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
	"""Count negation word. If odd, it is a negation tweet, return True, otherwise not."""
	
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
		return True,' '.join(new_tweet)
	else:
		return False,' '.join(new_tweet)

def remove_stop_words(tweet):
	"""Remove stop words."""

	stop_words = util.read_text_file(negation_words_file)
	tweet_words = tweet.split(' ')
	new_tweet = []

	for tweet_word in tweet_words:
		if tweet_word not in stop_words:
			new_tweet.append(tweet_word)

	return ' '.join(new_tweet)

def convert_emoticon(tweet):
	"""Convert emoticon to corresponding term."""
	
	# load from yaml, get dictionary
	emoticon_data = util.load_yaml_file(emoticons_file)
	
	# Replace emoticons
	for emoticon in emoticon_data.keys():
		tweet = tweet.replace(emoticon, emoticon_data[emoticon])

	return tweet

def get_levenshtein_distance(string_1, string_2):
	"""Return the levenshtein distance of two string."""

	if len(string_1) > len(string_2):
		string_1, string_2 = string_2, string_1

	if len(string_2) == 0:
		return len(string_1)

	first_length = len(string_1) + 1
	second_length = len(string_2) + 1

	distance_matrix = [[0] * second_length for x in range(first_length)]

	for i in range(first_length):
		distance_matrix[i][0] = i
		for j in range(second_length):
			distance_matrix[0][j] = j

	for i in xrange(1, first_length):
		for j in xrange(1, second_length):
			deletion_score = distance_matrix[i-1][j] + 1
			insertion_score = distance_matrix[i][j-1] + 1
			substitution_score = distance_matrix[i-1][j-1]

			if string_1[i-1] != string_2[j-1]:
				substitution_score += 1			
			
			distance_matrix[i][j] = min(insertion_score, deletion_score, substitution_score)

	return distance_matrix[first_length-1][second_length-1]

def preprocess_tweet(tweet):
	tweet = normalize_character(tweet)
	tweet = fold_case(tweet)
	tweet = remove_RT(tweet)
	tweet = remove_URL(tweet)
	tweet = remove_hashtag(tweet)
	tweet = remove_stop_words(tweet)
	tweet = remove_username(tweet)
	tweet = convert_number(tweet)
	tweet = convert_emoticon(tweet)
	tweet = clean_number(tweet)
	tweet = clean_one_char(tweet)
	negation, tweet = convert_negation(tweet)

	return negation, tweet

if __name__ == '__main__':
	tweet = 'Assalamu\'alaikum wrwb. Pagi rekan2. Kadang hati lbh hidup saat ingat kematian. Saat kebohongan tak lg diperlukan. Berkah, sehat & Semangat!'
	tweet = 'dtg aja pas futsal mingguan atau nonbar sob! :) RT @diezchocoalmee: @ICI_Bandung. Kapan N dmana sih anak" ic i suka ngmpul'

	# print get_levenshtein_distance('ronaldinho', 'rolando')
	print preprocess_tweet(tweet)
