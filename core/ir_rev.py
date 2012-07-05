#!/F3/core/info_rev.py
# This module is used for information retrieval function
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-16

from __future__ import division
from math import log
import util as util

class IR:

	def __init__(self, ingredients):
		'''Ingredients is a list of list of word.'''
		
		self.ingredients = ingredients

	def get_TF(self, word, idx):
		'''Get TF value of a word.'''
		
		if len(self.ingredients[idx]) == 0:
			return 0
		return self.ingredients[idx].count(word) / len(self.ingredients[idx])

	def get_IDF(self, word):
		'''Get IDF value of a word in ingredients.'''
		
		num_occur = 0
		for list_word in self.ingredients:
			if word in list_word:
				num_occur += 1
		if num_occur == 0:
			return 0
		else:
			return log(len(self.ingredients)/num_occur)

	def get_TF_IDF(self, word, idx):
		'''Get TF IDF value of a word in ingredients in a certain index.'''
		
		return self.get_TF(word, idx) * self.get_IDF(word)

	def get_dict_TF_IDF(self, idx, sort = True):
		'''Get dictionary contain all word in index idx and its TF IDF value and sorted by TF IDF value.'''	

		dict_TF_IDF = {}
		for word in set(self.ingredients[idx]):
			dict_TF_IDF[word] = self.get_TF_IDF(word, idx)

		if sort == True:
			retval = util.sort_dictionary_by_value(dict_TF_IDF)
			return retval
		else:
			return dict_TF_IDF


	def get_set_word(self):
		'''Return set of word in ingredients.'''

		retval = set()
		for list_word in self.ingredients:
			retval |= set(list_word)

		return retval
