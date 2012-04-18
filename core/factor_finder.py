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

class factor_finder:
	"""docstring for factor_finder"""

	def __init__(self, list_tweet):
		self.list_tweet = list_tweet
		self.memory = None
		
	def divide_sentiment_time(self, start_time, end_time, duration_hour = 1):
		"""Divide a list of sentiment by time, and get mean of each duration
			Return dictionary with key=each duration, value = sentiment."""

		duration_second = duration_hour * 3600
		delta_duration = datetime.timedelta(0, duration_second)
		len_end_start = end_time - start_time
		num_duration = (int)(ceil(len_end_start.total_seconds() / duration_second))
		temp_start = start_time

		retval = {}
		for i in xrange(0, num_duration):
			sent_time = {}
			temp_start += delta_duration
			sent_time['start_time'] = temp_start
			sent_time['end_time'] = temp_start + delta_duration
			sent_time['list_tweet'] = []
			sent_time['sentiment'] = 0
			retval[i] = sent_time

		# Add tweet
		for tweet in self.list_tweet:
			delta_tweet_time = tweet.time - start_time
			pos = (int)(floor(delta_tweet_time.total_seconds() / duration_second))
			if 0 <= pos < num_duration:
				retval[pos]['list_tweet'].append(tweet)

		# Get sentiment each duration
		for idx in retval.keys():
			sum_sentiment = 0
			mean_sentiment = 0
			for tweet in retval[idx]['list_tweet']:
				sum_sentiment += tweet.sentiment
			if len(retval[idx]['list_tweet']) != 0:
				mean_sentiment = sum_sentiment / len(retval[idx]['list_tweet'])
			else:
				mean_sentiment = 0
			retval[idx]['sentiment'] = mean_sentiment

		self.memory = retval
		self.start_time = start_time
		self.end_time = end_time
		self.duration_hour = duration_hour

		return retval

	def plot_graph(self):
		"""Plot Graph"""

		if self.memory == None:
			pass
		else:
			# Create graph
			# Title
			pylab.title('F3')
			pylab.xlabel('Time')
			pylab.ylabel('Sentiment')
			pylab.ylim(-1, 1)
			absis_data = []
			for idx in self.memory.keys():
				absis_data.append(self.memory[idx]['start_time'])
			ordinat_data = []
			for idx in self.memory.keys():
				ordinat_data.append(self.memory[idx]['sentiment'])
			pylab.plot(absis_data, ordinat_data)
			pylab.show()

	def get_break_points(self):
		"""Get break points"""
		retval = []
		if self.memory == None:
			pass
		else:
			for idx in self.memory.keys():
				if idx == 0 or idx == len(self.memory)-1:
					pass
				elif (self.memory[idx-1]['sentiment'] < self.memory[idx]['sentiment'] > self.memory[idx+1]['sentiment']) or (self.memory[idx-1]['sentiment'] < self.memory[idx]['sentiment'] > self.memory[idx+1]['sentiment']):
					retval.append(idx)

		return retval

	def clear_memory(self):
		"""Clear memory."""

		self.memory = None

	def create_ir_rev(self):
		"""Create ir_rev object. Need list of set of word in tweet from memory."""

		list_all_word = []
		for idx in self.memory.keys():
			words_time = []
			for tweet in self.memory[idx]['list_tweet']:
				if not tweet.parsed:
					tweet.preprocess()
				words_time.extend(tweet.parsed_word)
			list_all_word.append(words_time)

		ir_object = ir.IR(list_all_word)

		return ir_object

	def get_topics(self, idx, num_keywords = 5):
		"""get keyword as a topic from list_tweet in index idx"""

		if self.memory == None:
			pass
		else:
			ir_object = self.create_ir_rev()
			sorted_dict_TF_IDF = ir_object.get_dict_TF_IDF(idx)
			return sorted_dict_TF_IDF[:num_keywords]

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
	bp =  ff.get_break_points()
	for idx in bp:
		print 'keyword', idx
		print ff.get_topics(idx)
	ff.plot_graph()

if __name__ == '__main__':
	main()