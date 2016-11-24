import re
import sys
from pymongo import MongoClient
from datetime import datetime

file = open('/home/josn3503/Desktop/text.txt', 'r')
#print file.read()

client = MongoClient()
db = client.project
db.sensor_data

content_object = ""
ct_count = 1
prefix = "/unoise/utn/node2/"

for line in file:
		print "this is the start line" + "---------------------------"
		content_object = ""
		for in_line in file:

			if re.search("-----------------------------------------", in_line):
				result = db.sensor_data.insert_one({"prefix" : prefix+str(ct_count), "value": content_object})
				ct_count = ct_count+1
				print result
				print "-----ct begin"
				print content_object
				print "-----ct end"
				break
			content_object = content_object + in_line


result = db.sensor_data.insert_one({"value" : line})