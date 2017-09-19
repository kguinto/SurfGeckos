# SurfGeckos
(U) Source code for HACC 2017 contributions to Department of Health soil inspections

The ultimate goal is to automate the risk assessment of land intended for development based on soil analsis. Current procedures are found here:

 http://eha-web.doh.hawaii.gov/eha-cma/Leaders/HEER/environmental-hazard-evaluation-and-environmental-action-levels

This project builds upon and improves upon the spreadsheet `EAL Surfer (HDOH Summer 2016rev Jan 2017).xlsx`, found here: http://eha-web.doh.hawaii.gov/eha-cma/documents/b4061863-2cd0-4880-8af3-f969d71aa27a



From the command line 
```
git clone https://github.com/HACC17/SurfGeckos.git
cd SurfGeckos
virtualenv env
source env/bin/activate
pip install -r requirements.txt
cd djangosite
# create local .sqlite db
python manage.py migrate
# start server
python manage.py runserver
```

To view the user dialogue, go to 127.0.0.1:8000/

You can create a site with unrestricted use, drinking water, <150 from surface water and then print a pdf of the report from your browser.

HEER can modify data in the admin portion, 127.0.0.1:8000/admin

Everything works with SQLite by default. To use MongoDB, it must be installed and running on your computer. To run from a command line:
```
mongod
```

Auxillary files in the `src` directory:

* `excel2db.py`

	Loads excel file into MongoDB or SQLite database
	
	To use as a module:
	```
	from excel2db import Loader
	myfile = <excel file>
	mydb = <database name>
	Loader(myfile, mydb)
	```
	
	SQLite is the default. To use MongoDB:
	
	`Loader(myfile, mydb, mongo=True)`
	
	From the command line:

	`python excel2db.py <excel file>`
	
	OR
	
	`python excel2db.py <excel file> --mongo`

* `compiler.py`

	To use as a module:
	```
	from compiler import SurferReport
	report = SurferReport(input_data)
	report.record
	```

	From the command line (tests code on sample input):
	
	`python compiler.py`
