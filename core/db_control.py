#!/F3/core/db_control.py
# This file is used for accessing database
# Author : Ismail Sunni/@ismailsunni
# Created : 2012-03-23

import MySQLdb
import util as util

class db_conn:
	"""A class for controlling database connection."""

	# database variable
	db_host = 'localhost'
	db_user = 'root'
	db_password = ''
	db_name = 'tempe'
	
	def __init__(self):
		'''Initiate a db_conn class.'''

		self.conn = MySQLdb.connect(self.db_host, self.db_user, self.db_password, self.db_name)
		self.cursor = self.conn.cursor()

	def insert(self, list_table, dict_values):
		'''Insert to a database.'''
		
		if isinstance(list_table, str):
			list_table = [list_table]

		if not isinstance(list_table, list):
			list_table = list(list_table)

		for key in dict_values.keys():
			if dict_values[key] == None:
				values = 'NULL'
			else:
				values = str(dict_values[key])
				if len(values) == 0:
					values = "''"
				else:
					if values[0] != "'":
						values = "'" + values
					if  values[-1] != "'":
						values = values + "'"

			dict_values[key] = values

		columns = '(' + ', '.join(dict_values.keys()) + ')'
		values = '(' + ', '.join(dict_values.values()) + ')'
		tables = ', '.join(list_table)
		query = 'INSERT INTO ' + tables + ' ' + columns + ' VALUES ' + values

		try:
			self.cursor.execute(query)
			self.conn.commit()
			return True

		except Exception, e:
			util.debug('db_control.insert error' + str(e))
			self.conn.rollback()
			return False
			

	def read(self, list_table, list_column, list_filter):
		'''Read from database.'''

		if isinstance(list_table, str):
			list_table = [list_table]

		if not isinstance(list_table, list):
			list_table = list(list_table)

		columns = ', '.join(list_column)
		tables = ', '.join(list_table)
		filters = ' '.join(filters)
		query = 'SELECT ' + columns + ' FROM ' +  tables +  ' WHERE ' + filters

		try:
			self.cursor.execute(query)
			result = self.cursor.fetchall()

			return result

		except Exception, e:
			util.debug('db_control.read error' + str(e))
			self.conn.rollback()
			return None

	def delete(self, list_table, list_filter):
		'''Delete from database.'''

		if isinstance(list_table, str):
			list_table = [list_table]

		if not isinstance(list_table, list):
			list_table = list(list_table)

		tables = ', '.join(list_table)
		filters = ' '.join(list_filter)
		query = 'DELETE FROM ' +  tables +  ' WHERE ' + filters
		print query

		try:
			self.cursor.execute(query)
			self.conn.commit()

			return True
		except Exception, e:
			util.debug('db_control.delete error' + str(e))
			self.conn.rollback()
			return False


		pass
	
	def update(self, list_table, dict_values, list_filter):
		'''Update a database.'''
		# Not yet finished...

		if isinstance(list_table, str):
			list_table = [list_table]

		if not isinstance(list_table, list):
			list_table = list(list_table)


		for key in dict_values.keys():
			if dict_values[key] == None:
				values = 'NULL'
			else:
				values = str(dict_values[key])
				if len(values) == 0:
					values = "''"
				else:
					if values[0] != "'":
						values = "'" + values
					if  values[-1] != "'":
						values = values + "'"

			dict_values[key] = values

		sub_query = []
		for key in dict_values:
			sub_query.append(key + '=' + dict_values[key])

		sub_query = ', '.join(sub_query)
		tables = ', '.join(list_table)	
		filters = ' '.join(list_filter)
		query = 'UPDATE ' + tables + ' SET ' + sub_query + ' WHERE ' + filters

		print query

		try:
			self.cursor.execute(query)
			self.conn.commit()
			print 'True'
			return True

		except Exception, e:
			util.debug('db_control.insert error' + str(e))
			self.conn.rollback()
			return False

def main():
	conn = db_conn()

	table = 'barang'
	columns = ['harga_satuan', 'nama']
	# filters = ['harga_satuan > 5000', 'OR harga_satuan < 30000']
	filters = ['nama = menyang']
	# dict_values = {'nama':'menyang', 'harga_satuan':10000, 'kategori_id':1, 'path_gambar':'', 'jumlah':30}
	dict_values = {'harga_satuan':9999, 'kategori_id':1, 'path_gambar':'', 'jumlah':30}
	# conn.read(table, columns, filters)
	# if conn.insert(table, dict_values):
	# 	print 'succes'
	# filters = ['nama = "apem"', 'OR nama = "menyang"']
	# conn.update(table, dict_values, filters)
	conn.delete(table, filters)
	


if __name__ == '__main__':
	main()
