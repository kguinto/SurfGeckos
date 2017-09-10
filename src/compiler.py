"""
# From command line:
python compiler.py

# This will show sample output from sample data

# From within program

# define input_data as in the following example. It reprents user_input as in sheet 2.

	input_data = {
		"site_scenario":{
			"land_use":"Unrestricted",
			"groundwater_use":"Drinking Water Resource",
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

"""

help_ = """

We will work with mongodb by default.

A record will correspond to a specific project and chemical.
"""



class SurferReport:
	"""
	An object to represent the data found in Sheet labeled
	4. EAL Surfer - Surfer Report
	"""
	def __init__(self, input_data):
		"""
		"""
		self.record = self._create_record(input_data)

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
		"site_scenario":{"Site Name":__, "Site Address":__, "Site ID Number":__},
		"Site Scenario":{"land_use":__, "groundwater_use":__, "sw_distance":__},
		"Chemical of Concern":__,
		"Soil Environmental Hazards": __
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

			for key in soil_keys + other_soil_keys:
			
				out_data["soil_hazards"][key]["action_level"] = self._tier_1_action_level(key, input_data, chemical_data)
			for key in soil_keys:
				out_data["soil_hazards"][key]["potential_hazard"] = self._potential_hazard(key, chemical_data, out_data["soil_hazards"][key]["action_level"])
				out_data["soil_hazards"][key]["table"] = self._referenced_table(key, input_data, chemical_data)
			
			out_data["soil_hazards"][basis] = self._basis(chemical_data)
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

	def _basis(self, input_data):
		"""
		Placeholder function

		Surfer Compiler HDOH::Table 1::D25
		IF(C71=C70,"Background",(IF(C71=C46,B42,IF(C71=C50,B47,IF(C71=C56,B51,IF(C71=C60,B57,B61))))))
		C71=Final Tier 1 Soil EAL
		"""
		# TODO: This is just a placeholder
		return "Background"

	def _tier_1_action_level(self, key, input_data, chemical_data):
		"""
		PLACEHOLDER: Unfinished
		compiler - C46

		IF((IF(input_data["land_use"] == 'Unrestricted',C43,C44))=0,"-",(IF('2. EAL Surfer - Tier 1 EALs'::Table 1::D5='2. EAL Surfer - Tier 1 EALs'::Table 1::O13,C43,C44)))
		"""
		if input_data["site_scenario"]["land_use"]:
			# compiler C43
			result = 0
			#IF(VLOOKUP('2. EAL Surfer - Tier 1 EALs'::Table 1::H3,'Table I-1 (Unrestricted SoilDE)'::Table 1::A6:H159,2)=0,"-",VLOOKUP('2. EAL Surfer - Tier 1 EALs'::Table 1::H3,'Table I-1 (Unrestricted SoilDE)'::Table 1::A6:H159,2))
			
		else:
			# compiler - C44
			result = 0
			# IF(VLOOKUP('2. EAL Surfer - Tier 1 EALs'::Table 1::H3,'Table I-2 (C-I Soil DE)'::Table 1::A6:G159,2)=0,"-",VLOOKUP('2. EAL Surfer - Tier 1 EALs'::Table 1::H3,'Table I-2 (C-I Soil DE)'::Table 1::A6:G159,2))
		if result == 0:
			return '-'
		return result
	
	def _potential_hazard(self, key, input_data, tier_1_action_level):
		"""
		e.g. IF(F24="-","-",IF($D$19="-","-",(IF($D$19>F24,"Yes","No"))))
		"""
		try:
			soil = input_data["concentrations"]["soil"]
			if  float(soil) > float(tier_1_action_level):
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


if __name__ == '__main__':
	input_data = {
		"site_scenario":{
			"land_use":"Unrestricted",
			"groundwater_use":"Drinking Water Resource",
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
	
	report = SurferReport(input_data)
	print(report.record)
