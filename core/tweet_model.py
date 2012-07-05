#!/F3/core/tweet_model.py
# A class for representating a tweet.
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-03-30

from db_control import db_conn
from datetime import datetime, timedelta
import preprocess as pp

class tweet_model:
	'''A class for representating a tweet.'''
	
	def __init__(self, id, time, text, sentiment = 0, negation = 0):
		'''Standar __init__ function'''

		self.id = id
		self.time = time
		self.text = text
		self.negation = negation
		self.sentiment = sentiment
		self.parsed_word = []
		self.parsed = False
		self.post_parsed_word = []
		self.post_parsed = False	# this attribute indicate that the parsed_word has been preprocess again
		
	def print_tweet(self):
		'''Print procedure'''
		
		import unicodedata
		print unicodedata.normalize('NFKD', self.text.decode('latin-1')).encode('ascii', 'ignore'), self.sentiment

	def get_normal_text(self):
		'''Return content of the tweet in normal form.'''
		
		import unicodedata
		return unicodedata.normalize('NFKD', self.text.decode('latin-1')).encode('ascii', 'ignore')

	def preprocess(self, dict_param = None):
		'''Preprocess a tweet and save the result in parsed_word and negation.'''
		
		self.negation, preprocesssed_text = pp.preprocess_tweet(self.text, dict_param)
		self.parsed_word = preprocesssed_text.split(' ')
		self.parsed = True
		temp_post_parsed_word = pp.postparsed_text(preprocesssed_text)
		self.post_parsed_word = temp_post_parsed_word.split(' ')
		self.post_parsed = True

	
# public function	
def get_dev_data():
	'''Retrieve data from database for training and test as list of tweet object.'''

	db = db_conn()
	tweets = []

	query = "SELECT * FROM " + db.test_table + " WHERE `dev_tweet` = 1"
	retval = db.read(query)

	for row in retval:
		id = row[0]
		time = row[2]
		text = row[1]
		sentiment = row[3]
		negation = row[4]
		tweets.append(tweet_model(id, time, text, sentiment, negation))

	return tweets
	
def get_test_data(keyword = "", start_time = None, end_time = None):
	'''Retrieve data from database for training and test as list of tweet object.'''

	db = db_conn()
	tweets = []

	query = "SELECT * FROM " + db.test_table
	where = " WHERE `tweet_text` LIKE '%" + keyword + "%' AND `dev_tweet` != 1"
	if start_time != None:
		where += " AND `created_at` >= '" + start_time.__str__() + "'"
	if end_time != None:
		where += " AND `created_at` <= '" + end_time.__str__() + "'"
	
	order = " ORDER BY `created_at` ASC"
	
	retval = db.read(query + where)

	for row in retval:
		id = row[0]
		time = row[2]
		text = row[1]
		sentiment = row[3]
		negation = row[4]
		tweets.append(tweet_model(id, time, text, sentiment, negation))

	return tweets

def get_test_data_by_duration(keyword = "", start_time = None, end_time = None, duration_hour = 1):
	'''return test data divide byu duration.'''
	
	duration_second = duration_hour * 3600
	delta_duration = timedelta(0, duration_second)
	cur_time = start_time
	
	retval = []
	dur_times = []
	while (cur_time + delta_duration < end_time):
		retval.append(get_test_data(keyword, cur_time, cur_time + delta_duration))
		dur_times.append(cur_time)
		cur_time += delta_duration
		
	if (cur_time < end_time):
		dur_times.append(cur_time)
		retval.append(get_test_data(keyword, cur_time, end_time))
	
	return retval, dur_times

# main function for testing only
if __name__ == '__main__':
	keyword = "foke"
	start_time = datetime.strptime("10-4-2012 18:00:00", '%d-%m-%Y %H:%M:%S')
	end_time = datetime.strptime("18-4-2012 12:00:00", '%d-%m-%Y %H:%M:%S')
	duration_hour = 6
	
	retval, dur_times = get_test_data_by_duration(keyword, start_time, end_time, duration_hour)
	
	num_tweet = 0
	for ret in retval:
		print len(ret)
		num_tweet += len(ret)
	print num_tweet
	
	# write in excel
	from xlwt import Workbook
	from tempfile import TemporaryFile
	import util
	
	book = Workbook()
	
	try:
		sheet_idx = 1
		for list_tweet in retval:
			activeSheet = book.add_sheet(str(sheet_idx))
			
			activeSheet.write(0, 0, dur_times[sheet_idx - 1].__str__())
			
			i = 1
			activeSheet.write(i, 0, 'No')
			activeSheet.write(i, 1, 'Tweet Id')
			activeSheet.write(i, 2, 'Created')
			activeSheet.write(i, 3, 'Text')
			
			i += 1
			
			for tweet in list_tweet:
				activeSheet.write(i, 0, str(i - 1))
				activeSheet.write(i, 1, str(tweet.id))
				activeSheet.write(i, 2, tweet.time.__str__())
				activeSheet.write(i, 3, pp.normalize_character(tweet.text))
				i += 1
			
			sheet_idx += 1
		
		book.save('output.xls')
		book.save(TemporaryFile())
			
	except Exception, e:
		util.debug(str(e))
	
	print 'fin'