"""
Currently creates a databse of tables A through B2 (9-16)

From command line:
python excel2db.py <excel file> 
OR
python excel2db.py <excel file> --mongo

The former will created a sqlite database surfer.db.
The latter will work if mongodb is running and create a mongo db named surfer.

From within your own code

from excel2db import Loader
myfile = <excel file>
mydb = <database name>
Loader(myfile, mydb)
OR
Loader(myfile, mydb, mongo=True)



"""

########
# Table F-1 is very different and will need to be handled specially

###
import sys
import json
import argparse
import logging

import pandas

import openpyxl

logging_format = '%(asctime)s %(message)s'
logging.basicConfig(format=logging_format, level=logging.DEBUG)

# TODO: Explore sqlalchemy
# TODO: Make schema for all files

logging.debug("Begin")

##############################
# Establish table parameters #
##############################

A = ['contaminant', 'soil_far', 'groundwater_far', 'soil_close', 'groundwater_close']
C = ['contaminant', 'state_A', 'state_B', 'indoor_residential', 'indoor_commerical', 'shallow_residential', 'shallow_commercial']
D = ['contaminant', 'freshwater', 'marine', 'estuarine']
A1 = ['contaminant', 'eal', 'basis', 'gross_contamination', 'toxicity', 'background', 'direct_exposure', 'vapor_intrusion', 'drinking_water']
C1a = ['contaminant', 'state_A', 'state_B', 'unrestricted', 'commercial']
C1b = ['extra', 'contaminant', 'state_A', 'state_B', 'unrestricted', 'commercial']
C2 = ['contaminant', 'state_A', 'state_B', 'unrestricted_lowest', 'unrestricted_carcinogenic', 'unrestricted_noncarcinogenic', 'commercial_lowest', 'commercial_carcinogenic', 'commercial_noncarcinogenic']
C3 =  ['contaminant', 'state_A', 'state_B', 'urf', 'rfc', 'unrestricted_lowest', 'unrestricted_carcinogenic', 'unrestricted_noncarcinogenic', 'commercial_lowest', 'commercial_carcinogenic', 'commercial_noncarcinogenic']
D1a = ['contaminant', 'eal', 'basis', 'gross_contamination', 'toxicity', 'vapor_intrusion', 'aquatic_impacts']
E= ['contaminant', 'koc', 'koc_for_leaching', 'h', 'daf', 'saturation_limit', 'concentration_close_drinking', 'concentration_far_drinking',  'concentration_close_not_drinking', 'concentration_far_not_drinking', 'leaching_close_drinking', 'leaching_far_drinking',  'leaching_close_not_drinking', 'leaching_far_not_drinking',]


columns = {
	9:A,
	10:A,
	11:C,
	12:D,
	13:A1,
	14:A1,
	15:A1,
	16:A1,
	17:C1a,
	18:C1b,
	19:C2,
	20:C3,
	21:D1a,
	22:D1a,
	23:D1a,
	24:D1a,
	37:E,
	
	
	
} #sheet:names


###################
# parse arguments #
###################
def _parse_args():
	help_ = """Command line program to read in a single sheet from an excel file and upload to a database. It defaults to creating a sqlite database in the current directory with a provide name appened with ".db", with the default surfer.db
	
	The tables are hard to parse. The column names are not well lined-up, so I had trouble finding a consistent way to programmatically extract them.
	
	This code works on the sheet "Table A-1", sheet 13. I'll test on others later and adjust as needed. The default schema is the schema that works for Table A-1. Eventually, we should program in all the schemas.
	
	The --mongo flag will instead write to your mongodb.
	
	For this to work, mongodb needs to be running on your machine. On my mac, I used homebrew:
	brew install mongodb
I then needed to created the folder:
    /data/db
I could then run mongodb by typing:
    mongod
	"""

	parser = argparse.ArgumentParser(description=help_)
	parser.add_argument('input', help='path to EAL Surfer xlsx file')
	parser.add_argument('--skiprows', type=int, default=6,
						help="Number of nondatarows in the excel file, to include all headers, as the headers don't parse smoothly.")
	parser.add_argument('--names', default=None,
						help='comma-separated list of column names. The names for sheet 13 will default')
	parser.add_argument('--sheet', default=13, type=int,
						help='Sheet number to draw from (0-based). Data tables start with sheet 13.')
	parser.add_argument('--mongohost', default='localhost',
						help='host where mongodb server is running')
	parser.add_argument('--mongoport', default=27017, type=int,
						help='port where mongodb server is running')
	parser.add_argument('--db', default='surfer',
						help='name of  database')
	parser.add_argument('--collection', default='a1',
						help='name of collection/table')
	parser.add_argument('--mongo', action='store_true',
						help='uses mongodb instead of sqllite')
	args = parser.parse_args()

	if args.names:
		names=arg.names
	else:
		names = [
			"CHEMICAL PARAMETER", "FINAL EAL", "BASIS", "Table F-2",
			"Table L", "Table K", "Table I-1", "Table C-1b", "Table E"
		]
	return args, names
	

####################
# Read excel sheet #
####################

def read_excel(workbook, names, sheet, skiprows, skipfooter):
	df = pandas.read_excel(
		workbook,
        sheetname=sheet,
        header=None,
		skiprows=skiprows,
		skipfooter=skipfooter,
        names=names # Doesn't seem to be doing what I want
    )
	df.columns = names # Shouldn't be needed, but names=names above not working right for me.
	return df

def get_sheetnames(workbook):
	"""

	"""
	return  {i:name
			 for i,name in enumerate(workbook.sheetnames)
			 if name.startswith('Table') or name.startswith('Summary')}

def get_skiprows(workbook, sheets):
	"""
	Skip the the first row containing ACENAPHTHENE or #ACENAPHTHENE
	Headers can't be automatically derived
	"""
	result = {}
	for sheetnum in sheets:
		sheet = workbook.worksheets[sheetnum]
		for i,row in enumerate(sheet.rows):
			try:
				if 'ACENAPHTHENE' in row[0].value:
					result[sheetnum]=list(range(i))
					break
			except TypeError:
				pass
	return result

def get_skipfooter(workbook, sheets):
	result = {}
	for sheetnum in sheets:
		sheet = workbook.worksheets[sheetnum]
		result[sheetnum] = []
		done = False
		for i, row in enumerate(sheet.rows):
			try:
				if 'ZINC' in row[0].value:
					done = True
					continue
				if done:
					result[sheetnum].append(i)
			except TypeError:
				pass
	return {sheet:len(rows) for sheet, rows in result.items()}
	

######################
# Upload to database #
######################

def sqlite_load(df, db_name, table, names, safe=False):

	logging.debug("Loading to sqlite {} {}".format(db_name, table))
	import sqlite3
	conn = sqlite3.connect(db_name)
	c = conn.cursor()

	try:
		create_command='''CREATE TABLE "{}" {}'''.format(table, tuple(names))
		c.execute(create_command)
	except sqlite3.OperationalError:
		# Probably the table exists
		if safe:
			# Stop loading the data
			return
		else:
			# Destroy the table
			c.execute('drop table "{}"'.format(table))
			c.execute(create_command)
		# An alternative is to allow the new data to be inserted
	
	insert_command = 'INSERT INTO "{}" VALUES ({})'.format(table,','.join(['?']*len(names)))
	c.executemany(insert_command, df.itertuples(index=False, name=None))
	conn.commit()

	# To test
	c.execute('SELECT * from "{}"'.format(table))
	logging.debug(c.fetchone())

def mongo_load(df, db_name, collection_name,
			   mongohost='localhost', mongoport=27017):
	"""
	Assumes mongodb is running on machine
	"""
	logging.debug("Loading to mongo {} {}".format(db_name, collection_name))
	from pymongo import MongoClient

	records =  json.loads(df.T.to_json()).values()
	
	client = MongoClient(mongohost, mongoport)
	db = client[db_name]
	collection = db[collection_name]
	collection.insert_many(records)

	# To test
	logging.debug(collection.find_one())


def load_sheet_2(workbook, db_name, collection_name, mongo=False, startrow=32, startcol='M', lastcol='Y'):
	"""
	"""

	columns = None 
	df = None
	if mongo:
		mongo_load(df, db_name, collection_name)
	else:
		sqlite_load(df, db_name, collection_name, columns)


	
class Loader:
	"""

	"""
	def __init__(self, workbook_file, db_name, sheets=range(9,16), mongo=False, sheet2=False):
		"""
		tables in sheets 9-51
		"""
		self.workbook_file = workbook_file
		self.sheets = sheets
		self.db_name = db_name
		workbook = openpyxl.load_workbook(workbook_file)
		self.collections = get_sheetnames(workbook)
		self.skiprows = get_skiprows(workbook, sheets)
		self.skipfooter = get_skipfooter(workbook, sheets)
		workbook.close()
		if sheet2:
			load_sheet_2(workbook_file, "auxillary", "auxillary", mongo)
		self._load(mongo)
	def _load(self, mongo):
		"""
		"""
		for sheet in self.sheets:
			logging.debug("Loading sheet {}".format(sheet))
			try:
				df = read_excel(self.workbook_file,
								columns[sheet], sheet, self.skiprows[sheet],
								self.skipfooter[sheet]
				)
			except TypeError:
				logging.debug(columns[sheet])
				logging.debug(sheet)
				logging.debug(self.skiprows[sheet])
				logging.debug(self.skipfooter[sheet])
				sys.exit(1)
			
			if mongo: # Use mongodb
				mongo_load(df, self.db_name, self.collections[sheet])

			else: # Use sqlite3
				sqlite_load(df, self.db_name,
							self.collections[sheet],
							columns[sheet])			
		
		

if __name__ == '__main__':

	args, names = _parse_args()
	Loader(args.input, args.db, mongo=args.mongo)


	# df = read_excel(args.input, names, args.sheet, args.skiprows)
	
	# if args.mongo: # Use mongodb
	# 	mongo_load(df, args.db, args.collection)

	# else: # Use sqlite3
	# 	db_name = args.db+ ".db"
	# 	table_name = "table_" + str(args.sheet)
	# 	sqlite_load(df, db_name, table_name, names)
	
# Finished




