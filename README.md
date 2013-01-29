bosreport
=========

Create (monthly) structure reports based on SWDES Equidistant (LDB)
files. Python 2.7 is required to run this program.


Installation
------------

- Install Python 2.7

- Put bosreport somewhere


Usage
-----

1. Place .ldb files in the input folder. Examples can be found in the test
folder.

2. Run bosreport.py, optionally using bosreport.bat.

3. Find your output files in the output folder.

4. Copy draaiuren_template.xls to a new file for each file in the output dir
and copy the contents of an output csv into Sheet 1.

5. If you want to fiddle around, run 'python bosreport.py -h' for help.
