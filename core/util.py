# !/F3/core/util.py
# util function
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-03-23

import operator


# defaul values
debug_mode = 1

def debug(message, mode=debug_mode):
	'''debug mode.'''

	if mode == 1:
		print '__debug__', message

# getter
def get_from_dictionary(keyword, dictionary, default_value=0):
	'''Getter function for dictionary. If keyword is not in dictionary, return default_value'''

	if keyword in dictionary:
		return dictionary[keyword]
	else:
		return default_value

def sort_dictionary_by_value(dictionary, descending = True, num_returned = -1):
	'''Sort dictionary to a list.

		@parameter
		@dictionary = the dictionary
		@descending = descending if true, otherwise ascending
		@num_returned = number of element returned. default_value = -1, all.'''

	retval = sorted(dictionary.iteritems(), key=operator.itemgetter(1), reverse = descending)
	if num_returned > len(dictionary):
		return retval
	else:
		return retval[0:num_returned]

# converter
def convert_list_of_tuple_to_dictionary(list_of_tuple):
	'''Convert list of tuple to dictionary.'''

	retval = dict()
	for tup in list_of_tuple:
		retval[tup[0]] = tup[1]
		
	return retval

# print
def print_index_list_dict(list_or_dict):
	'''Print index and element of a list or dictionary.'''

	for index, item in enumerate(list_or_dict):
		print index, item

# read external file
def read_text_file(file_path):
	'''Read external text file.

		Return list of string in each line.'''
	try:
		f = open(file_path)
		list_of_string = f.readlines()
		f.close()

		return list_of_string
	except Exception, e:
		debug('read_text_file' + str(e))
		return None
	