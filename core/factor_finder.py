#!/F3/core/factor_finder.py
# This module is used for finding a factor
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-16


from __future__ import division
from math import ceil, floor
import pylab
import datetime
import tweet_model as tm
import ir_rev as ir
import util as util
import pickle
from copy import deepcopy

class factor_finder:
	'''docstring for factor_finder'''

	def __init__(self, list_tweet, keyword = ""):
	
		self.list_tweet = list_tweet
		self.memory = None
		self.keyword = keyword
		self.start_time = None
		self.end_time = None
		self.duration_hour = None
		self.break_points = None
		
	def divide_sentiment_time(self, start_time, end_time, duration_hour = 1, factor = 0.5):
		'''Divide a list of sentiment by time, and get mean of each duration
			Return dictionary with key=each duration, value = sentiment.'''

		duration_second = duration_hour * 3600
		delta_duration = datetime.timedelta(0, duration_second)
		len_end_start = end_time - start_time
		num_duration = (int)(ceil(len_end_start.total_seconds() / duration_second))
		temp_start = start_time

		retval = {}
		for i in xrange(0, num_duration):
			sent_time = {}
			sent_time['start_time'] = temp_start
			sent_time['end_time'] = temp_start + delta_duration
			sent_time['list_tweet'] = []
			sent_time['sentiment'] = 0
			sent_time['cum_sentiment'] = 0
			retval[i] = sent_time
			temp_start += delta_duration

		# Add tweet
		for tweet in self.list_tweet:
			delta_tweet_time = tweet.time - start_time
			pos = (int)(floor(delta_tweet_time.total_seconds() / duration_second))
			if 0 <= pos < num_duration:
				retval[pos]['list_tweet'].append(tweet)

		# Get sentiment each duration
		for idx in retval.keys():
			sum_sentiment = 0
			num_sentiment = 0
			mean_sentiment = 0
			for tweet in retval[idx]['list_tweet']:
				if tweet.sentiment != 0:
					sum_sentiment += tweet.sentiment
					num_sentiment += 1
			if num_sentiment != 0:
				mean_sentiment = sum_sentiment / len(retval[idx]['list_tweet'])
				# mean_sentiment = sum_sentiment / num_sentiment
			else:
				mean_sentiment = 0
			
			if idx != 0:
				retval[idx]['cum_sentiment'] = factor * retval[idx - 1]['cum_sentiment'] + (1 - factor) * mean_sentiment
			else:
				retval[idx]['cum_sentiment'] = mean_sentiment
				
			retval[idx]['sentiment'] = mean_sentiment
			retval[idx]['num_tweet_sentiment'] = num_sentiment

		self.memory = retval
		self.start_time = start_time
		self.end_time = end_time
		self.duration_hour = duration_hour

		return retval

	def plot_graph(self):
		'''Plot Graph'''

		if self.memory == None:
			pass
		else:
			# Create graph
			# Title
			pylab.title('F3')
			pylab.xlabel('Time')
			pylab.ylabel('Sentiment')
			
			absis_data = []
			for idx in self.memory.keys():
				absis_data.append(self.memory[idx]['start_time'])
			
			ordinat_data = []
			for idx in self.memory.keys():
				ordinat_data.append(self.memory[idx]['cum_sentiment'])
			
			pylab.ylim(-1, 1)
					
			pylab.plot(absis_data, ordinat_data)
			pylab.show()

	def get_break_points(self):
		'''Get break points'''
		
		retval = []
		if self.memory == None:
			pass
		else:
			for idx in self.memory.keys():
				if idx == 0 or idx == len(self.memory)-1:
					pass
				elif (self.memory[idx-1]['cum_sentiment'] < self.memory[idx]['cum_sentiment'] > self.memory[idx+1]['cum_sentiment']) or (self.memory[idx-1]['cum_sentiment'] > self.memory[idx]['cum_sentiment'] < self.memory[idx+1]['cum_sentiment']):
					retval.append(idx)
		
		self.break_points = retval
		
		return retval

	def clear_memory(self):
		'''Clear memory.'''

		self.memory = None
		self.start_time = None
		self.end_time = None
		self.duration_hour = None


	def create_ir_rev(self, sentiment = 1):
		'''Create ir_rev object. Need list of set of word in tweet from memory.'''

		list_all_word = []
		for idx in self.memory.keys():
			words_time = []
			for tweet in self.memory[idx]['list_tweet']:
				if tweet.sentiment == sentiment:
					if not tweet.parsed:
						tweet.preprocess()
					words_time.extend(tweet.post_parsed_word)
			list_all_word.append(words_time)

		list_all_word = util.remove_all_values_from_list(list_all_word, self.keyword)
		list_all_word = util.remove_all_values_from_list(list_all_word, ' ')
		list_all_word = util.remove_all_values_from_list(list_all_word, '')
		
		ir_object = ir.IR(list_all_word)

		return ir_object

	def get_topics(self, idx, num_keywords = 5, sort = True, sentiment = 1):
		'''get keyword as a topic from list_tweet in index idx'''

		if self.memory == None:
			util.debug('memory empty')
			return None
			
		else:
			ir_object = self.create_ir_rev(sentiment)
			if sort == True:
				sorted_dict_TF_IDF = ir_object.get_dict_TF_IDF(idx, True)
				return sorted_dict_TF_IDF[:num_keywords]
			else:
				unsorted_dict_TF_IDF = ir_object.get_dict_TF_IDF(idx, False)
				return unsorted_dict_TF_IDF
			

	def get_all_topics(self, num_keywords = 5, decay_factor = 0.5, sentiment = 1):
		'''get all topic for each duration. Using decay factor.'''
		
		list_keywords = {}
		if self.memory == None:
			util.debug('memory empty')
			return None
		
		else:
			for idx in self.memory.keys():
				list_keywords[idx] = self.get_topics(idx, 100, False, sentiment)
		
		retval = {}
		for idx in list_keywords.keys():
			keywords = {}
			if idx == 0:
				for keyword in list_keywords[idx]:
					keywords[keyword] = list_keywords[idx][keyword]
			else:
				for keyword in list_keywords[idx]:
					if retval[idx-1].has_key(keyword):
						# decay factor
						keywords[keyword] = (list_keywords[idx][keyword]) + (decay_factor * retval[idx-1][keyword])
					else:
						keywords[keyword] = list_keywords[idx][keyword]
			retval[idx] = keywords
		
		final_retval = {}
		for r in retval.keys():
			final_retval[r] = util.sort_dictionary_by_value(retval[r])[:num_keywords]
		
		super_final_retval = {}
		for r in final_retval.keys():
			super_final_retval[r] = [final_retval[r][i][0] for i in xrange(0, len(final_retval[r]))]
		
		return super_final_retval
		
	def get_break_point_topics(self, num_topics = 5):
		'''get keyword as a topic from each breakpoint.'''
		
		if self.memory == None or self.break_points == None:
			util.debug('memory empty')
			return None
			
		else:
			retval = {}
			for idx in self.break_points:
				temp_retval = self.get_topics(idx, num_topics)
				retval[idx] = [temp_retval[i][0] for i in xrange(0, len(temp_retval))]
			
			return retval 
			
	# save and load
	def save(self, file_name):
		'''Save factor finder, especially list tweet.'''
		
		try:
			if not file_name.endswith('.pickle'):
				file_name += '.pickle'
			f = open(file_name, 'wb')
			pickle.dump(self, f)
			f.close()
			return True
			
		except Exception, e:
			util.debug("save factor finder error. " + str(e))
			return False
	
	def load(self, file_name):
		'''Load factor finder, especially list tweet.'''
		
		try:
			f = open(file_name)
			self = deepcopy(pickle.load(f))
			f.close()
			return True, self
			
		except Exception, e:
			util.debug("load factor finder error. " + str(e))
			return False, None
		pass
	
	
# testing function
def main():
	t1 = tm.tweet_model(1, datetime.datetime(2012, 04, 13, 13, 8, 7), 'Finka, Si Seksi yang Doyan Ngebut ', 1)
	t2 = tm.tweet_model(2, datetime.datetime(2012, 04, 13, 15, 18, 37), 'OSO Securities: IHSG akan Kembali Menguat', -1)
	t3 = tm.tweet_model(3, datetime.datetime(2012, 04, 13, 15, 31, 54), 'Ikutan Yuk LIVECHATkustik Bareng ADA Band di detikForum', 1)
	t4 = tm.tweet_model(4, datetime.datetime(2012, 04, 13, 15, 31, 54), 'RT @len_hineni \(^_^)/ pegi kmna ko ipi?? RT @flip3011: @Phi09979 @Grania_FN mggu dpn aku blk jogja, tp lgsg brgkt lg. Kyke masih bi...', 1)
	t5 = tm.tweet_model(5, datetime.datetime(2012, 04, 13, 11, 31, 54), 'Jian rempeyek!!', -1)
	ff = factor_finder([t1, t2, t3, t4, t5])
	s = datetime.datetime(2012, 4, 13, 11, 0, 15)
	e = datetime.datetime(2012, 4, 13, 18, 0, 14)
	retval = ff.divide_sentiment_time(s, e, 2)
	for idx in ff.memory.keys():
		print idx, 'sentiment : ', ff.memory[idx]['sentiment']
		
	for idx in ff.memory.keys():
		print ff.memory[idx]

	bp =  ff.get_break_points()
	for idx in bp:
		print 'keyword', idx
		print ff.get_topics(idx)
	# ff.plot_graph()

if __name__ == '__main__':
	main()