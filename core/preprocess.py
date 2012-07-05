#!/F3/core/preprocess.py
# This file is used for preprocessing
# static function
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-03-30

import re
import unicodedata
import util as util
import ttp	# module from https://github.com/BonsaiDen/twitter-text-python
import string

# Global variables
negation_words_file = "negation_words.yaml"	# Created by ismailsunni
stop_words_file = "stop_words.yaml"			# Created by ismailsunni
emoticons_file = "emoticons.yaml"			# Created by ismailsunni
synonyms_file = "synonyms.yaml"				# Created by ismailsunni

def normalize_character(tweet_text):
    '''Normalize a string from unicode character.'''

    return unicodedata.normalize('NFKD', tweet_text.decode('latin-1')).encode('ascii', 'ignore')

def remove_punctuation_word(tweet_word):
	'''Remove punctuation in a word.'''

	punctuations = string.punctuation + '\n'

	if not (tweet_word in ['_e_pos_', '_e_sad_']):
		for punct in punctuations:
			tweet_word = tweet_word.replace(punct, '')
	
	return tweet_word

def remove_punctuation_string(tweet_text):
	'''Remove punctuation in a tweet_text.

		Please use convert_emoticon first'''

	tweet_words = tweet_text.split(' ')
	retval = []
	for tweet_word in tweet_words:
		retval.append(remove_punctuation_word(tweet_word))

	return ' '.join(retval)

def fold_case(tweet_text):
	'''Fold case of a string.'''
	
	return tweet_text.lower()
	
def remove_RT(tweet_text):
	'''Obvious function.'''

	regex_RT = r'(\A|\s)(RT|rt)(\s|\Z)'
	tweet_text = re.sub(regex_RT, ' ', tweet_text)
	
	return tweet_text

def remove_username(tweet_text):
	'''Obvious function.'''

	p = ttp.Parser()
	users = p.parse(tweet_text).users
	for user in users:
		tweet_text = tweet_text.replace('@'+user, '')

	return tweet_text

def remove_URL(tweet_text):
	'''Obvious function.'''	

	p = ttp.Parser()
	urls = p.parse(tweet_text).urls
	for url in urls:
		tweet_text = tweet_text.replace(url, '')

	return tweet_text

def remove_hashtag(tweet_text):
	'''Obvious function.'''	

	p = ttp.Parser()
	tags = p.parse(tweet_text).tags
	for tag in tags:
		tweet_text = tweet_text.replace('#'+tag, tag)

	return tweet_text

def clean_number(tweet_text):
	'''Clean number from tweet_text. Number which is cleaned is stand-alone, begining of word, and end of word number.'''

	regex_begin = r'(\A| )\d+'
	regex_end = r'\d+( |\Z|\z)'
	regex_space = r'\s{2,}'

	tweet_text = re.sub(regex_begin, ' ', tweet_text)
	tweet_text = re.sub(regex_end, ' ', tweet_text)
	tweet_text = re.sub(regex_space, ' ', tweet_text)

	return tweet_text

def clean_one_char(tweet_text):
	'''Clean a character surround by whitespace.'''

	# bug found
	# regex_one_char = r'\s+\S\s+'

	# tweet_text = re.sub(regex_one_char, ' ', tweet_text)

	words = tweet_text.split(' ')
	words_temp = []

	for word in words:
		if len(word) > 1:
			words_temp.append(word)

	tweet_text = ' '.join(words_temp)

	return tweet_text

def convert_number(tweet_text):
	'''Convert number to certain character.'''

	tweet_text = tweet_text.replace('00', 'u')
	tweet_text = tweet_text.replace('0', 'o')
	tweet_text = tweet_text.replace('1', 'i')
	tweet_text = tweet_text.replace('3', 'e')
	tweet_text = tweet_text.replace('4', 'a')
	tweet_text = tweet_text.replace('5', 's')
	tweet_text = tweet_text.replace('6', 'g')
	tweet_text = tweet_text.replace('7', 't')
	tweet_text = tweet_text.replace('8', 'b')
	tweet_text = tweet_text.replace('9', 'g')

	new_tweet_text = []

	for i in xrange(0,len(tweet_text)):
		if tweet_text[i] != '2':
			new_tweet_text.append(tweet_text[i])
		else:
			new_tweet_text.append(tweet_text[i-1])

	return ''.join(new_tweet_text)

def convert_negation(tweet_text):
	'''Count negation word. If odd, it is a negation tweet_text, return True, otherwise not.'''
	
	negation_words = util.load_yaml_file(negation_words_file)
	num_negation_word = 0
	new_tweet_text = []
	tweet_text_words = tweet_text.split(' ')

	for tweet_word in tweet_text_words:
		if tweet_word in negation_words:
			num_negation_word += 1
		else:
			new_tweet_text.append(tweet_word)
	
	if num_negation_word % 2 == 1:
		return True,' '.join(new_tweet_text)
	else:
		return False,' '.join(new_tweet_text)

def remove_stop_words(tweet):
	'''Remove stop words.'''

	stop_words = util.load_yaml_file(stop_words_file)
	tweet_words = tweet.split(' ')
	new_tweet = []

	for tweet_word in tweet_words:
		if tweet_word not in stop_words:
			new_tweet.append(tweet_word)

	return ' '.join(new_tweet)

def convert_emoticon(tweet):
	'''Convert emoticon to corresponding term.'''
	
	# load from yaml, get dictionary
	emoticon_data = util.load_yaml_file(emoticons_file)
	
	# Replace emoticons
	for emoticon in emoticon_data.keys():
		tweet = tweet.replace(emoticon, ' ' + emoticon_data[emoticon] + ' ')

	return tweet

def convert_word(tweet):
	'''Convert word to corresponding term.'''
	
	# load from yaml, get dictionary
	synonym_data = util.load_yaml_file(synonyms_file)
	
	# Replace word
	for synonym in synonym_data.keys():
		tweet = tweet.replace(synonym, ' ' + synonym_data[synonym] + ' ')

	return tweet	

def get_levenshtein_distance(string_1, string_2):
	'''Return the levenshtein distance of two string.'''

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

def is_near(string_1, string_2, max_distance = 1):
	'''Return true if two is string has levenshtein distance no more than max_distance.'''

	return get_levenshtein_distance(string_1, string_2) <= max_distance

def is_near_words(string, list_string, max_distance = 1):
	'''Return true if there is string that has levenshtein distance no more than max_distance.'''
	
	for word in list_string:
		if is_near(word, string, max_distance):
			return True

	return False

def postparsed_text(tweet_text, dict_param = None):
	'''Postparsed is used to makesure foldcase, no punctuation, no RT for factor finder process, no username.'''
	
	if dict_param == None:	
		tweet_text = fold_case(tweet_text)
		tweet_text = remove_RT(tweet_text)
		tweet_text = remove_username(tweet_text)
		tweet_text = remove_punctuation_string(tweet_text)
		# tweet_text = remove_stop_words(tweet_text)
		# tweet_text = convert_word(tweet_text)
	
	else:
		if dict_param['fold_case'] == 0:
			tweet = fold_case(tweet)				# 1			
		if dict_param['remove_RT'] == 0:
			tweet = remove_RT(tweet)				# 2
		if dict_param['remove_username'] == 0:
			tweet = remove_username(tweet)		# 9
		if dict_param['remove_punctuation_string'] == 0:
			tweet = remove_punctuation_string(tweet)# 7
		#if dict_param['convert_word'] == 0:
		#	tweet = convert_word(tweet)		# 13
		#if dict_param['remove_stop_words'] == 0:
		#	tweet = remove_stop_words(tweet)	
	
	return tweet_text
	
def preprocess_tweet(tweet, dict_param = None):
	negation = False
	if dict_param == None:
		tweet = normalize_character(tweet) 		# 0 wajib
		tweet = remove_URL(tweet)				# 3 wajib	
		tweet = clean_one_char(tweet)			# 11 wajib

		return negation, tweet

	else:
		tweet = normalize_character(tweet) 		# 0 wajib

		if dict_param['fold_case'] == 1:
			tweet = fold_case(tweet)				# 1			
		if dict_param['remove_RT'] == 1:
			tweet = remove_RT(tweet)				# 2
		
		tweet = remove_URL(tweet)				# 3 wajib

		if dict_param['remove_hashtag'] == 1:
			tweet = remove_hashtag(tweet)			# 4
		if dict_param['remove_username'] == 1:
			tweet = remove_username(tweet)		# 9
		if dict_param['convert_number'] == 1:
			tweet = convert_number(tweet)			# 10
		if dict_param['clean_number'] == 1:
			tweet = clean_number(tweet)			# 6
		if dict_param['convert_emoticon'] == 1:
			tweet = convert_emoticon(tweet)		# 5
		if dict_param['remove_punctuation_string'] == 1:
			tweet = remove_punctuation_string(tweet)# 7
		if dict_param['convert_word'] == 1:
			tweet = convert_word(tweet)		# 13
		if dict_param['remove_stop_words'] == 1:
			tweet = remove_stop_words(tweet)		# 8

		tweet = clean_one_char(tweet)			# 11	wajib

		if dict_param['convert_negation'] == 1:
			negation, tweet = convert_negation(tweet)# 12

		return negation, tweet

# main function for testing only
if __name__ == '__main__':
	tweet = 'Assalamu\'alaikum wrwb. Pagi rekan2. Kadang hati lbh hidup saat ingat kematian. Saat kebohongan tak lg diperlukan. Berkah, sehat & Semangat!'
	tweet = 'tau di tidak RT dtg aja pas futsal mingguan atau no\nbar sob! :) RT @diezchocoalmee: @ICI_Bandung. Kapan N dmana sih anak" ic i suka ngmpul di rumah pak RT lho'

	# print get_levenshtein_distance('ronaldinho', 'rolando')
	print preprocess_tweet(tweet)
