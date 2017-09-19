"""
# From command line:
python compiler.py

# This will show sample output from sample data

# From within program

# define input_data as in the following example. It reprents user_input as in sheet 2.

	input_data = {
		"site_scenario":{
			"land_use":"Unrestricted",
			"groundwater_use":"drinking", #not_drinking
			"sw_distance":"not_close", #close
			"name":"My house",
			"address":"123 Happy Place",
			"site_id":"553423",
			"timestamp":0
		},
		"contaminants":
		[
			{
				"choice":"Chemical Name",
				"contaminant":"ACENAPHTHENE",
				"concentrations":
				{
					"soil":10,
					"groundwater":10,
					"soil_vapor":10,
				}
			}
		],
	}

from compiler import SurferReport
report = SurferReport(input_data)
report.record

# report.record will be a dictionary with the data found in spreadsheet 4

# Sample output:

{
	'site_scenario':
	{
		'land_use': 'Unrestricted',
		'groundwater_use': 'Drinking Water Resource',
		'sw_distance': 'not_close',
		'name': 'My house',
		'address': '123 Happy Place',
		'site_id': '553423',
		'timestamp': 0
	},
	'contaminants':
	[{
		'concentrations':
		{
			'soil': 10,
			'groundwater': 10,
			'soil_vapor': 10
		},
		'contaminant': 'ACENAPHTHENE',
		'soil_hazards':
		{
			'direct_exposure':
			{
				'units': 'mg/kg',
				'action_level': '-',
				'potential_hazard': '-',
				'table': 'Table I-1'
			},
			'vapor_emissions':
			{
				'units': 'mg/kg',
				'action_level': '-',
				'potential_hazard': '-',
				'table': 'Table C-1b'
			},
			'ecotoxicity':
			{
				'units': 'mg/kg',
				'action_level': '-',
				'potential_hazard': '-',
				'table': 'Table L'
			},
			'gross_contamination':
			{
				'units': 'mg/kg',
				'action_level': '-',
				'potential_hazard': '-',
				'table': 'Table F-2'
			},
			'leaching':
			{
				'units': 'mg/kg',
				'action_level': '-',
				'potential_hazard': '-',
				'table': 'Table E-1'
			},
			'background':
			{'units': 'mg/kg',
			 'action_level': '-'
			},
			'eal':
			{
				'units': 'mg/kg',
				'action_level': '-'
			},
			'basis': 'Background'
		}
	}
	]
}
"""

import json
import sys
import logging

logging_format = '%(asctime)s %(message)s'
logging.basicConfig(format=logging_format, level=logging.INFO)

help_ = """

We will work with mongodb by default.

A record will correspond to a specific project and chemical.
"""

def db_lookup(value, db, table, field, mongo=False):
	if mongo:
		return mongo_lookup(value, db, table, field)
	else:
		sqlite_lookup(value, db, table, field)

def mongo_lookup(value, db, collection, field):
	try:
		result = next(db[collection].find({"contaminant":value}))
	except StopIteration:
		logging.info("Cannot find {} in {}".format(value, collection))
		return -1
	return result[field]

def is_float(x):
	try:
		float(x)
		return True
	except:
		return False

def sqlite_lookup(value, db, table, field):
	query_command = "SELECT {} FROM {} WHERE contaminant=?".format(field, table)
	cursor = db.cursor()
	cursor.execute(query_command, value)



class SurferReport:
	"""
	An object to represent the data found in Sheet labeled
	4. EAL Surfer - Surfer Report
	"""
	
	def __init__(self, input_data, db_name, mongo=True):
		"""
		"""
		self.db_name = db_name
		self.mongo = mongo # boolean
		self.db = self._db_connect('localhost', 27017)
		self.record = self._create_record(input_data)

	def _db_connect(self, mongohost, mongoport):
		if self.mongo:
			from pymongo import MongoClient
			client = MongoClient(mongohost, mongoport)

			return client[self.db_name]
			
		else:
			import sqlite3
			return sqlite3.connect(self.db_name)
			
	def to_db(self, mongohost, mongoport, database, collection_name):
		"""
		"""
		client = MongoClient(mongohost, mongoport)
		db = client[database]
		collection = db[collection_name]
		collection.insert(self.record)

	def _create_record(self, input_data):
		"""
		Produces a record such as:

		{
		"site_scenario":{"name":__, "address":__, "site_id":__, "land_use":__, "groundwater_use":__, "sw_distance":__},
		:contaminants:[{"contaminant":__,
		"concentrations":__,
		"soil_hazards": __}]
		}
		"""
		concentration_keys = [
			"soil",
			"groundwater",
			"soil_vapor"
		]
		soil_contamination_unit = "mg/kg"
		soil_keys = [
			"direct_exposure",
			"vapor_emissions",
			"ecotoxicity",
			"gross_contamination",
			"leaching"
		]
		other_soil_keys = [
			"background",
			"eal"
		]
		basis = "basis"
		record = {}
		#
		record["site_scenario"] = input_data["site_scenario"]
		#
		record["site_scenario"] = input_data["site_scenario"]
		#
		record["contaminants"] = []
		
		#
		
		for chemical_data in input_data["contaminants"]:
			# Example of chemical_data
			# {
			# 	"choice":"Chemical Name",
			# 	"contaminant":"ACENAPHTHENE",
			# 	"site_scenario":
			# 	{
			# 		"soil":10,
			# 		"groundwater":10,
			# 		"soil_vapor":10,
			# 	}
			# }
			out_data = {}
			out_data["concentrations"] = {}
			out_data["contaminant"] = self._chemical_of_concern(chemical_data)
			for key in concentration_keys:
				out_data["concentrations"][key] = self._concentration(key, chemical_data)

			#

			out_data["soil_hazards"] = {}
			for key in soil_keys + other_soil_keys:
				out_data["soil_hazards"][key] = {}
				out_data["soil_hazards"][key]["units"] = soil_contamination_unit

			for key in soil_keys:
			
				out_data["soil_hazards"][key]["action_level"] = self._tier_1_action_level(key, input_data, chemical_data)
				out_data["soil_hazards"][key]["potential_hazard"] = self._potential_hazard(key, chemical_data, out_data["soil_hazards"][key]["action_level"])
				out_data["soil_hazards"][key]["table"] = self._referenced_table(key, input_data, chemical_data)

			out_data["soil_hazards"]["background"] = self._background(chemical_data["contaminant"])
			lowest = self._lowest_soil_eal(out_data["soil_hazards"], soil_keys)
			out_data["soil_hazards"][basis] = lowest[0]
			out_data["soil_hazards"]["eal"]["action_level"] = self._final_eal(lowest[1], out_data["soil_hazards"]["background"])
			record['contaminants'].append(out_data)
		return record

	def _chemical_of_concern(self, input_data):
		"""
		Spreadsheet "4. EAL Surfer - Surfer Report"
		Cell E-H 16
		References Spreadsheet 2, H3
		if D14=N27, C16, (VLOOKUP (C16, N33:)186,2,0)
		"""
		if input_data["choice"]=="Chemical Name":
			
			return input_data["contaminant"]
		else:
			# TODO: Look up by CAS#
			# Will need that table in a separate database
			raise NotImplementedError("Currently only supports lookup by chemical name")

	def _concentration(self, key, input_data):
		"""
		For soil, Spreadsheet 4, D19
		IF('2. EAL Surfer - Tier 1 EALs'::Table 1::D22=0,"-",'2. EAL Surfer - Tier 1 EALs'::Table 1::D22)
		"""
		value = input_data["concentrations"][key]
		if not value:
			# TODO: This is what currently exists.
			# Perhaps better null value would be better
			return "-"
		return value

		
	def _tier_1_action_level(self, key, input_data, chemical_data):
		"""

		"""
		if key=='leaching':
			return self._leaching_eal(input_data, chemical_data)
		tables = {
			"vapor_emissions":'Table C-1b (Soil to IA)',
			"ecotoxicity":'Table L (Soil Ecotoxicity)',
			"gross_contamination":'Table F-2 (Exposed Soils)'
		}
		
		fields = {
			"vapor_emissions":("unrestricted", "commercial"),
			"ecotoxicity":("residential", "commercial"),
			"gross_contamination":("final_unrestricted_action_level",
								   "final_commercial_action_level")
		}
		

		if input_data["site_scenario"]["land_use"]=="Unrestricted":
			if key=="direct_exposure":
				table = "Table I-2 (C-I Soil DE)"
				field = "eal"
			else:
				table = tables[key]
				field = fields[key][0]
		else:
			if key=="direct_exposure":
				table = "Table I-2 (C-I Soil DE)"
				field = "eal"
			else:
				table = tables[key]
				field = fields[key][1]
		result = self._db(chemical_data["contaminant"],
						  table,
						  field)
		if result == 0:
			return '-'
		return result

	def _final_eal(self, lowest, background):
		"""
		"""
		if background in ["?", "-"]:
			return lowest
		return max(float(background), float(lowest))
			
	
	def _potential_hazard(self, key, input_data, eal):
		"""
		e.g. IF(F24="-","-",IF($D$19="-","-",(IF($D$19>F24,"Yes","No"))))
		"""
		try:
			soil = input_data["concentrations"]["soil"]
			if  float(soil) > float(eal):
				return "Yes"
			else:
				return "No"
		except ValueError:
			return "-"

	def _referenced_table(self, key, input_data, chemical_data):
		"""
		
		"""
		reference_tables = {
			"direct_exposure":"Table I-1" if input_data["site_scenario"]["land_use"]=="Unrestricted" else "Table I-2",
			"vapor_emissions":"Table C-1b",
			"leaching":"Table E-1",
			"ecotoxicity":"Table L",
			"gross_contamination": "Table F-2",
		}
		return reference_tables[key]

	def _background(self, contaminant):
		"""
		compiler C70
		"""
		table =  "Table K (Soil Background)"
		if self._db(contaminant, "auxillary", "code")==2:
			
			result = self._db(contaminant,
							  table,
							  "action_level")
			if not result:
				return "?"
		else:
			return "-"

	def _leaching_eal(self, input_data, chemical_data):
		"""
		placeholder
IF(
IF(E28="YES",
   C52,
   IF(E29="YES",
      C53,
      IF(E30="YES",
          C54,
          C55)))=0,"-",IF(E28="YES",C52,IF(E29="YES",C53,IF(E30="YES",C54,C55))))
		"""
		
		fields = {
			('close', 'drinking'):'leaching_close_drinking',
			('close', 'not_drinking'):'leaching_close_not_drinking',
			('not_close', 'drinking'):'leaching_far_drinking',
			('not_close', 'not_drinking'): 'leaching_far_not_drinking',
		}
		table = "Table E Leaching"

		result = self._db(chemical_data["contaminant"],
						  table,
						  fields[(input_data["site_scenario"]["sw_distance"],
								  input_data["site_scenario"]["groundwater_use"])])
		if result == 0:
			return '-'
		return result
		

	def _lowest_soil_eal(self, hazards, keys):
		"""
		input should be out_data["soil_hazards"]
		returns key, eal
		"""
		return min(
			(
				(key, float(hazards[key]["action_level"]))
				for key in keys
				if is_float(hazards[key]["action_level"])
			),
			key=lambda __:__[1]
		)

	def _db(self, value, table, field):
		return db_lookup(value, self.db, table, field, self.mongo)



if __name__ == '__main__':
	input_data = {
		"site_scenario":{
			"land_use":"Unrestricted",
			"groundwater_use":"drinking", #not_drinking
			"sw_distance":"not_close", #close
			"name":"My house",
			"address":"123 Happy Place",
			"site_id":"553423",
			"timestamp":0
		},
		"contaminants":
		[
			{
				"choice":"Chemical Name",
				"contaminant":"ACENAPHTHENE",
				"concentrations":
				{
					"soil":10,
					"groundwater":10,
					"soil_vapor":10,
				}
			}
		],
	}
	
	report = SurferReport(input_data, db_name="surfer", mongo=False)
	print(json.dumps(report.record, indent=4))
