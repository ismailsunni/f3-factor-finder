#!/F3/core/run_it.py
# This file is used for creating a script
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-04-06

import MySQLdb				# accesing mysql database
from xlwt import Workbook	# for writing in excel
import xlrd 				# for reading excel
from tempfile import TemporaryFile
import util as util
import tweet_model as tm
import preprocess as pp
from db_control import db_conn

def main_sql_to_excel():
	"""Read from database then write in excel"""

	# To do
	# read database

	# database variable
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'rimus'

	conn = MySQLdb.connect(db_host, db_user, db_password, db_name)
	cursor = conn.cursor()

	query = "SELECT * FROM `tweets`"
	try:
		cursor.execute(query)
		result = cursor.fetchall()
		# return result

	except Exception, e:
		util.debug('db_control.read error' + str(e))
		conn.rollback()
		result = None

	# write to excel
	book = Workbook()
	activeSheet = book.add_sheet('tweets')
	i = 1
	activeSheet.write(i, 0, 'No')
	activeSheet.write(i, 1, 'Tweet Id')
	activeSheet.write(i, 2, 'Username')
	activeSheet.write(i, 3, 'Created')
	activeSheet.write(i, 4, 'Text')
	
	from random import sample
	result = sample(result, 3000)

	i += 1
	try:
		for row in result:
			activeSheet.write(i, 0, str(i - 1))
			activeSheet.write(i, 1, str(row[0]))
			activeSheet.write(i, 2, str(row[7]))
			activeSheet.write(i, 3, row[3].__str__())
			activeSheet.write(i, 4, pp.normalize_character(row[1]))
			i += 1
			# print i
			if i >= 50002:
				break

		book.save('test_data_training2.xls')
		book.save(TemporaryFile())

	except Exception, e:
		util.debug(str(e))

def main_excel_to_sql():
	book = xlrd.open_workbook('test_data_training2.xls')
	sheet = book.sheet_by_name('tweets')

	tweets = []
	for row in range(sheet.nrows):
		if sheet.row_values(row)[5] == 1:
			new_data = {}
			new_data['id'] = int(sheet.row_values(row)[1])
			new_data['sentiment'] = int(sheet.row_values(row)[4])
			tweets.append(new_data)

	# new_db = new db_conn()

	print tweets

def move_data():
	book = xlrd.open_workbook('data_training_TA_Ismail Sunni.xls')
	sheet = book.sheet_by_name('tweets')

	tweets = []
	k = 0
	for row in range(sheet.nrows):
		if sheet.row_values(row)[6] == 3:
			tweets.append(sheet.row_values(row))

	conn = db_conn()

	i = 0
	for tweet in tweets:
		query = "INSERT INTO " + conn.dev_table + "( `tweet_id`, `tweet_text`, `created_at`, `sentiment`) VALUES (" + str(tweet[1]) + ", '" + tweet[4] + "', '" + tweet[3] + "', '" + str(int(tweet[5])) +"')"
		# print query
		if conn.insert(query) == True:
			i += 1
	print i

def ultimate_function():
	book = xlrd.open_workbook('data_training_TA_Ismail Sunni.xls')
	sheet = book.sheet_by_name('tweets')	

	tweets = []
	for row in range(sheet.nrows):
		if sheet.row_values(row)[6] == 3:
			tweets.append(sheet.row_values(row))

	conn = db_conn()

	i = 0
	j = 0
	for tweet in tweets:
		query = "UPDATE " + conn.test_table + " SET `sentiment`=" + str(int(tweet[5])) + ", `dev_tweet`= 1 WHERE `tweet_id`="+str(tweet[1])
		if conn.update(query) == True:
			i += 1
		else:
			j += 1
	print i
	print j

def reset_data():
	conn = db_conn()
	query = "UPDATE " + conn.test_table + " SET `dev_tweet` = 0"
	return conn.update(query)



if __name__ == '__main__':
	print reset_data()
	ultimate_function()
	