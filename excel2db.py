import json
import argparse
import pandas

# TODO: Explore sqlalchemy
# TODO: Make schema for all files

###################
# parse arguments #
###################

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
parser.add_argument('--skiprows', type=int, default=6, help="Number of nondatarows in the excel file, to include all headers, as the headers don't parse smoothly.")
parser.add_argument('--names', default=None, help='comma-separated list of column names. The names for sheet 13 will default')
parser.add_argument('--sheet', default=13, type=int, help='Sheet number to draw from (0-based). Data tables start with sheet 13.')
parser.add_argument('--mongohost', default='localhost', help='host where mongodb server is running')
parser.add_argument('--mongoport', default=27017, type=int, help='port where mongodb server is running')
parser.add_argument('--db', default='surfer', help='name of  database')
parser.add_argument('--collection', default='a1', help='name of collection/table')
parser.add_argument('--mongo', action='store_true', help='uses mongodb instead of sqllite')
args = parser.parse_args()

if args.names:
	names=arg.names
else:
	names = ["CHEMICAL PARAMETER", "FINAL EAL", "BASIS", "Table F-2",
			 "Table L", "Table K", "Table I-1", "Table C-1b", "Table E"
	]
	

####################
# Read excel sheet #
####################


df = pandas.read_excel(args.input,
                  sheetname=args.sheet,
                  header=None,
					   skiprows=list(range(args.skiprows)),
                  names=names # Doesn't seem to be doing what I want
                 )
df.columns = names # Shouldn't be needed, but names=names above not working right for me.
df

records = json.loads(df.T.to_json()).values()

######################
# Upload to database #
######################


if args.mongo: # Use mongodb
	from pymongo import MongoClient
	client = MongoClient(args.mongohost, args.mongoport)
	db = client[args.db]
	collection = db[args.collection]
	collection.insert_many(records)

	# To test
	print(collection.find_one())
else: # Use sqlite3
	import sqlite3
	conn = sqlite3.connect(args.db + ".db")
	c = conn.cursor()
	table = "table_" + str(args.sheet)
	try:
		create_command = "CREATE TABLE {} {}".format(table, tuple(names))
		c.execute(create_command)
	except sqlite3.OperationalError:
		# Probably means you already created the table
		pass
	
	insert_command = 'INSERT INTO {} VALUES ({})'.format(table,','.join(['?']*len(names)))
	c.executemany(insert_command, df.itertuples(index=False, name=None))
	conn.commit()

	# To test
	c.execute("SELECT * from {}".format(table))
	print(c.fetchone())
				  
	
# Finished




