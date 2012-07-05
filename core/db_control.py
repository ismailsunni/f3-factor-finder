#!/F3/core/db_control.py
# This file is used for accessing database
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-03-23

import MySQLdb
import util as util
import preprocess as pp

class db_conn:
	'''A class for controlling database connection.'''

	# database variable
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'rimus'

	# table
	dev_table = 'dev_table'
	test_table = 'test_table'
	
	def __init__(self):
		'''Initiate a db_conn class.'''

		self.conn = MySQLdb.connect(self.db_host, self.db_user, self.db_password, self.db_name)
		self.cursor = self.conn.cursor()

	def read(self, query):
		'''Read database.'''

		try:
			self.cursor.execute(query)
			retval = self.cursor.fetchall()

			return retval

		except Exception, e:
			util.debug('db_control.read error : ' + str(e))
			self.conn.rollback()

			return None

	def insert(self, query):
		'''Insert to database.'''

		try:
			self.cursor.execute(query)
			self.conn.commit()

			return True

		except Exception, e:
			util.debug('db_control.insert error: ' + str(e))
			self.conn.rollback()

			return False

	def delete(self, query):
		'''Delete row(s) in database.'''

		try:
			self.cursor.execute(query)
			self.conn.commit()

			return True

		except Exception, e:
			util.debug('db_control.delete error : ' + str(e))
			self.conn.rollback()
		
			return False

	def update(self, query):

		try:
			self.cursor.execute(query)
			self.conn.commit()

			return True

		except Exception, e:
			util.debug('db_control.update error : ' + str(e))
			self.conn.rollback()
		
			return False


	# Public Functions
	def get_dev_data(self):
		'''Retrieve data from database for training and test.'''
		
		query = "SELECT * FROM " + self.dev_table

		try:
			self.cursor.execute(query)
			data = self.cursor.fetchall()

			retval = []

			for row in data:
				new_row = {}
				new_row['id'] = row[0]
				new_row['time'] = row[2]
				new_row['text'] = row[1]
				new_row['negation'] = row[4]
				new_row['sentiment'] = row[3]
				retval.append(new_row)

			return retval


		except Exception, e:
			util.debug('db_control.read error' + str(e))
			self.conn.rollback()
			return None
		
	def get_test_data(self):
		'''Retrieve data to be predicted from database'''
		query = "SELECT * FROM " + self.test_table + " LIMIT 0, 100"

		try:
			self.cursor.execute(query)
			data = self.cursor.fetchall()

			retval = []
			
			for row in data:
				new_row = {}	
				new_row['id'] = row[0]
				new_row['time'] = row[2]
				new_row['text'] = row[1]
				new_row['negation'] = row[4]
				new_row['sentiment'] = row[3]
				retval.append(new_row)

			return retval

		except Exception, e:
			util.debug('db_control.read error' + str(e))
			self.conn.rollback()
			return None

# testing function
def main():
	conn = db_conn()

	retval = conn.get_test_data()
	print len(retval)

	i = 0
	for row in retval:
		print i, pp.normalize_character(row['text'])
		i += 1
		if i > 100:
			break

if __name__ == '__main__':
	main()
