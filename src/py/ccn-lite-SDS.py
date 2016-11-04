# ccn-lite/src/py/ccn-lite-SDS.py

'''
Copyright (C) 2015, JOhan SNider, Uppsala University

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

File history:
2015-11-2 created
'''
import json

import ccnlite.client
nw = ccnlite.client.Access()

projectPrefixString = "unoise"
locPrefixArray = ['utn','foobar']
seqnoPrefixArray = ['1','2','3','4','5','6']

firstPrefix = '/'+ projectPrefixString +'/'+ locPrefixArray[0] +'/'+ seqnoPrefixArray[0]

sensor_ip = "127.0.0.1"
sensor_port = 9999
#sensor_prefix = "/demo/mote1"

nw.connect(sensor_ip, sensor_port)
pkts = nw.getLabeledContent(firstPrefix, raw=False) 
#tolkens = pkts[0].split("-", 4)

data_store = [[]]

i = 0

#request 6 items of sensor data for every location
for location in locPrefixArray:
	for seqno in seqnoPrefixArray:
		currPrefix = '/'+ projectPrefixString +'/'+ location +'/'+ seqno
		print currPrefix
		pkts = nw.getLabeledContent(currPrefix, raw=False) 
		print pkts[0]
		print "i: " + str(i)
		data_store[i].append(pkts[0])
	i = i+1
	data_store.append([])

#build sensor data object
activeSensorArray = [[]]
i=0
for location in locPrefixArray:
	#print data_store[0][0]
	if (int(data_store[i][0]) >= 0):
		#print location + ' is active' 
		activeSensorArray[i].append(location)
		#how long is row
		#print location + ' length: ' + str(len(data_store[i]))
		activeSensorArray[i].append(len(data_store[i]))
	i = i+1
	activeSensorArray.append([])

'''
TODO: build a json object
#build json object
json_sensor_data = "{sensor_data:[{'"

for location in activeSensorArray:
	print location[0]

	#json_sensor_data = json_sensor_data + str(location[0]) + " ':' " +  str(location[0]) + " ' },"


json_sensor_data = json_sensor_data + "]}" 

print json_sensor_data

json_data = json.dumps(activeSensorArray)
'''

#TODO: create a content object of that sensor_data json

#TODO: store values in data base

#TODO: do prediction stuff and make content objects

print activeSensorArray
print data_store

print json_data





