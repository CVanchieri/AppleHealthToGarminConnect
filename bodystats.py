#!/usr/bin/env python3

# run to create csv.
# ./bodystats.py > bodystats_garmin.csv

# imports.
from datetime import datetime
import xml.etree.ElementTree as ET

# parse _cda data.
export_cda = ET.parse('export_cda.xml')
# get root _cda data.
export_cda_root = export_cda.getroot()
# parse _cda data.
export = ET.parse('export.xml')
# get root _cda data.
export_root = export.getroot()

#####

# print titles for dataframe.
print("")
print("Body")
print("Date,Weight,BMI,Fat")

# set the features.
weight_dict = {}
bmi_dict = {}
fat_dict = {}

for record in export_root.findall('Record'):
	start_date = datetime.strptime(record.get('startDate'), '%Y-%m-%d %H:%M:%S %z')
	date_string = start_date.strftime('%Y-%m-%d')
	value = record.get('value')

	# get the weight.
	if(record.get('type') == "HKQuantityTypeIdentifierBodyMass"):
		if date_string in weight_dict:
			weight_dict[date_string] = float(weight_dict[date_string]) + float(value)
		else:
			weight_dict[date_string] = float(value)
	# get the bmi.
	if(record.get('type') == "HKQuantityTypeIdentifierBodyMassIndex"):
		if date_string in bmi_dict:
			bmi_dict[date_string] = float(bmi_dict[date_string]) + float(value)
		else:
			bmi_dict[date_string] = float(value)
	# get the bodyfat.
	if(record.get('type') == "HKQuantityTypeIdentifierBodyFatPercentage"):
		if date_string in fat_dict:
			fat_dict[date_string] = float(fat_dict[date_string]) + float(value)
		else:
			fat_dict[date_string] = float(value)

# iterate over all dates in weight.
for date_key in weight_dict:
	output = "\""
	output += date_key
	output += "\",\""

	# weight.
	if date_key in weight_dict:
			output += str(round(weight_dict[date_key],2))
	else:
			output += "0"
	output += "\",\""
	# bmi.
	if date_key in bmi_dict:
			output += str(round(bmi_dict[date_key],2))
	else:
			output += "0"
	output += "\",\""
	# bodyfat.
	if date_key in fat_dict:
			output += str(round(fat_dict[date_key]* 100,2))
	else:
			output += "0"
	output += "\""

	# print results.
	print(output)