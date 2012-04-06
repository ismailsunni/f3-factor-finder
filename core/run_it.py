#!/F3/core/run_it.py
# This file is used for creating a script
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-03-23

import MySQLdb				# accesing mysql database
from xlwt import Workbook	# for write in excel
from tempfile import TemporaryFile
import util as util
import tweet_model as tm
import preprocess as pp

def main_sql_to_excel():
	"""Read from database then write in excel"""

	# To do
	# read database

	# database variable
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'tweet_f3'

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
	activeSheet.write(i, 2, 'Created')
	activeSheet.write(i, 3, 'Text')
	
	from random import sample
	result = sample(result, 500)

	i += 1
	try:
		for row in result:
			activeSheet.write(i, 0, str(i - 1))
			activeSheet.write(i, 1, str(row[0]))
			activeSheet.write(i, 2, row[2].__str__())
			activeSheet.write(i, 3, pp.normalize_character(row[1]))
			i += 1
			# print i
			if i >= 50002:
				break

		book.save('test_data_training.xls')
		book.save(TemporaryFile())

	except Exception, e:
		util.debug(str(e))

if __name__ == '__main__':
	main_sql_to_excel()