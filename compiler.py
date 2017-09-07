# Unfinished. Doesn't do anything yet.
# Haven't even tested. Just want to show you where my mind is.

help_ = """
Expecting json, e.g.
input_data = 
{
"Site Scenario":{"Land Use":__, "Groundwater Utility":__, "Distance To Nearest Surface Water Body":__,},
"Contaminant":{"Chemical Name or CAS#":__, "Contaminant":__},
{"Site Data":{"Soil (mg/kg)":__, "Groundwater (ug/L)":__, "Soil Vapor (ug/m^3":__}},
"Site Information":{"Site Name":__, "Site Address":__, "Site ID Number":__}
}	input_data = {
		"Site Scenario":{
			"Land Use":"Unrestricted",
			"Groundwater Utility":"Drinking Water Resource",
			"Distance To Nearest Surface Water Body":"< 150m",
		},
		"Contaminant":{
			"Chemical Name or CAS\#":"Chemical Name",
			"Contaminant":"ACENAPHTHENE",
		},
		"Site Data":{
			"Soil (mg/kg)":10,
			"Groundwater (ug/L)":10,
			"Soil Vapor (ug/m^3":10,
		},
		"Site Information":{
			"Site Name":"My house",
			"Site Address":"123 Happy Place",
			"Site ID Number":"553423",
		}
	}

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
		"Site Information":{"Site Name":__, "Site Address":__, "Site ID Number":__},
		"Site Scenario":{"Land Use":__, "Groundwater Utility":__, "Distance To Nearest Surface Water Body":__},
		"Chemical of Concern":__,
		"Soil Environmental Hazards": __
		}
		"""
		record = {}
		#
		record["Site Information"] = input_data["Site Information"]
		#
		record["Site Scenario"] = input_data["Site Scenario"]
		#
		record["Chemical of Concern"] = self._chemical_of_concern(input_data)
		#
		record["Input Site Concentrations"] = {}
		concentration_keys = [
			"Soil (mg/kg)",
			"Groundwater (ug/L)",
			"Soil Vapor (ug/m^3"
		]
		for key in concentration_keys:
			record["Input Site Concentrations"][key] = self._concentration(key, input_data)

		#
		soil_contamination_unit = "mg/kg"
		soil_keys = [
			"Direct Exposure",
			"Vapor Emissions to Indoor Air",
			"Terrestrial Ecotoxicity",
			"Gross Contamination",
			"Leaching (threat to groundwater)"
		]
		other_soil_keys = [
			"Background",
			"Final Soil Tier 1 EAL"
		]
		basis = "Basis"
		record["Soil Environmental Hazards"] = {}
		for key in soil_keys + other_soil_keys:
			record["Soil Environmental Hazards"][key] = {}
			record["Soil Environmental Hazards"][key]["Units"] = soil_contamination_unit

		for key in soil_keys + other_soil_keys:
			
			record["Soil Environmental Hazards"][key]["Tier 1 Action Level"] = self._tier_1_action_level(key, input_data)
		for key in soil_keys:
			record["Soil Environmental Hazards"][key]["Potential Hazard?"] = self._potential_hazard(key, input_data, record["Soil Environmental Hazards"][key]["Tier 1 Action Level"])
			record["Soil Environmental Hazards"][key]["Referenced Table"] = self._referenced_table(key, input_data)
			
		record["Soil Environmental Hazards"][basis] = self._basis(input_data)
		
		return record

	def _chemical_of_concern(self, input_data):
		"""
		Spreadsheet "4. EAL Surfer - Surfer Report"
		Cell E-H 16
		References Spreadsheet 2, H3
		if D14=N27, C16, (VLOOKUP (C16, N33:)186,2,0)
		"""
		if input_data["Contaminant"]["Chemical Name or CAS\#"]=="Chemical Name":
			
			return input_data["Contaminant"]["Contaminant"]
		else:
			# TODO: Look up by CAS#
			# Will need that table in a separate database
			raise NotImplementedError("Currently only supports lookup by chemical name")

	def _concentration(self, key, input_data):
		"""
		For soil, Spreadsheet 4, D19
		IF('2. EAL Surfer - Tier 1 EALs'::Table 1::D22=0,"-",'2. EAL Surfer - Tier 1 EALs'::Table 1::D22)
		"""
		value = input_data["Site Data"][key]
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

	def _tier_1_action_level(self, key, input_data):
		"""
		PLACEHOLDER: Unfinished
		compiler - C46

		IF((IF(input_data["Land Use"] == 'Unrestricted',C43,C44))=0,"-",(IF('2. EAL Surfer - Tier 1 EALs'::Table 1::D5='2. EAL Surfer - Tier 1 EALs'::Table 1::O13,C43,C44)))
		"""
		if input_data["Site Scenario"]["Land Use"]:
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
			
		return 0
	def _potential_hazard(self, key, input_data, tier_1_action_level):
		"""
		e.g. IF(F24="-","-",IF($D$19="-","-",(IF($D$19>F24,"Yes","No"))))
		"""
		try:
			soil = input_data["Site Data"]["Soil (mg/kg)"]
			if  float(soil) > float(tier_1_action_level):
				return "Yes"
			else:
				return "No"
		except ValueError:
			return "-"

	def _referenced_table(self, key, input_data):
		"""
		
		"""
		reference_tables = {
			"Direct Exposure":"Table I-1" if input_data["Site Scenario"]["Land Use"]=="Unrestricted" else "Table I-2",
			"Vapor Emissions to Indoor Air":"Table C-1b",
			"Leaching (threat to groundwater)":"Table E-1",
			"Terrestrial Ecotoxicity":"Table L",
			"Gross Contamination": "Table F-2",
		}
		return reference_tables[key]


if __name__ == '__main__':
	input_data = {
		"Site Scenario":{
			"Land Use":"Unrestricted",
			"Groundwater Utility":"Drinking Water Resource",
			"Distance To Nearest Surface Water Body":"< 150m",
		},
		"Contaminant":{
			"Chemical Name or CAS\#":"Chemical Name",
			"Contaminant":"ACENAPHTHENE",
		},
		"Site Data":{
			"Soil (mg/kg)":10,
			"Groundwater (ug/L)":10,
			"Soil Vapor (ug/m^3":10,
		},
		"Site Information":{
			"Site Name":"My house",
			"Site Address":"123 Happy Place",
			"Site ID Number":"553423",
		}
	}
	report = SurferReport(input_data)
	print(report.record)
