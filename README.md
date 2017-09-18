# SurfGeckos
(U) Source code for HACC 2017 contributions to Department of Health soil inspections

This project builds upon and improves upon the spreadsheet `EAL Surfer (HDOH Summer 2016rev Jan 2017).xlsx`, found here: (add link)

From the command line within the project folder
```
virtualenv env
source env/bin/activate
pip -r requirements.txt
```

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
