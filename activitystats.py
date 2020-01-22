#!/usr/bin/env python3

# run to create csv.
# ./activitystats.py > activitystats_garmin.csv

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
print("Activities")
print("Date,Calories Burned,Steps,Distance,Floors,Minutes Sedentary,Minutes Lightly Active,Minutes Fairly Active,Minutes Very Active,Activity Calories")

# set features.
steps_dict = {}
distance_dict = {}
floors_dict = {} 

for record in export_root.findall('Record'):
	start_date = datetime.strptime(record.get('startDate'), '%Y-%m-%d %H:%M:%S %z')
	date_string = start_date.strftime('%Y-%m-%d')
	value = record.get('value')

	# get the steps.
	if(record.get('type') == "HKQuantityTypeIdentifierStepCount"):
		if date_string in steps_dict:
			steps_dict[date_string] = int(steps_dict[date_string]) + int(value)
		else:
			steps_dict[date_string] = int(value)
	# get the distances.
	if(record.get('type') == "HKQuantityTypeIdentifierDistanceWalkingRunning"):
		if date_string in distance_dict:
			distance_dict[date_string] = float(distance_dict[date_string]) + float(value)
		else:
			distance_dict[date_string] = float(value)
	# get the floors.
	if(record.get('type') == "HKQuantityTypeIdentifierFlightsClimbed"):
		if date_string in floors_dict:
			floors_dict[date_string] = int(floors_dict[date_string]) + int(value)
		else:
			floors_dict[date_string] = int(float(value))

# iterate over all dates in steps.
for date_key in steps_dict:
	output = "\""
	output += date_key
	output += "\",\"0\",\""

	# steps.
	if date_key in steps_dict:
			output += str("{:,}".format(steps_dict[date_key]))
	else:
			output += "0"
	output += "\",\""
	# distances.
	if date_key in distance_dict:
			output += str(round(distance_dict[date_key],2))
	else:
			output += "0"
	output += "\",\""
	# floors.
	if date_key in floors_dict:
			output += str(floors_dict[date_key])
	else:
			output += "0"
	output += "\",\"0\",\"0\",\"0\",\"0\",\"0\""

	# print results.
	print(output)
