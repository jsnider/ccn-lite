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

Setup:

0) build fake content object ie run create_fake_data.sh (make sure is executable ie chmod 777 create_fake_data.sh)
1) start B router:
	$CCNL_HOME/bin/ccn-lite-relay -v trace -s ndn2013 -u 9999 -x /tmp/mgmt-relay-b.sock -d $CCNL_HOME/test/ndntlv
2) test with normal peek, you should get back 45
	$CCNL_HOME/bin/ccn-lite-peek -s ndn2013 -u 127.0.0.1/9999 "/unoise/foobar/node1/1" | $CCNL_HOME/bin/ccn-lite-pktdump	

'''
import json

import ccnlite.client
nw = ccnlite.client.Access()

projectPrefixString = "unoise"
locPrefixArray = ['utn','foobar', 'rullan']
nodePreficArray = ['node1', 'node2']
seqnoPrefixArray = ['1','2','3','4']

#firstPrefix = '/'+ projectPrefixString +'/'+ locPrefixArray[0] +'/'+ seqnoPrefixArray[0]

relay_ip = "127.0.0.1"
relay_port = 9999
#sensor_prefix = "/demo/mote1"

nw.connect(relay_ip, relay_port)
#pkts = nw.getLabeledContent('/unoise/utn/node1/2', raw=False) 
#tolkens = pkts[0].split("-", 4)
#print pkts[0]


data_store = [[[]]]

i = 0 # for location
j = 0 # for node
#request 6 items of sensor data for every location
for location in locPrefixArray:
	j = 0 # for node
	for node in nodePreficArray:
		for seqno in seqnoPrefixArray:
			currPrefix = '/'+ projectPrefixString +'/'+ location +'/'+ node +'/' + seqno
			print currPrefix
			pkts = nw.getLabeledContent(currPrefix, raw=False) 
			print pkts[0]
			print 'j: ' + str(j)
			print 'i: ' + str(i)
			print data_store
			data_store[i][j].append(pkts[0].rstrip('\r\n'))
		j = j+1
		data_store[i].append([])
	i = i+1
	data_store.append([[]])

print data_store #TODO store this in a database
# example output [['90', '60', '40', '20', '85', '65', '45', '15'], ['45', '50', '60', '70', '43', '52', '63', '69'], ['200', '250', '300', '400', '180', '275', '280', '420'], []]

#build sensor data object
'''
activeSensorArray = [[]]
i=0
for location in locPrefixArray:
	#print data_store[0][0]
	if (int(data_store[i][0]) >= 0): #if the data_store array has a value for a node then the node is alive typ
		#print location + ' is active' 
		activeSensorArray[i].append(location)
		#how long is row
		#print location + ' length: ' + str(len(data_store[i]))
		activeSensorArray[i].append(len(data_store[i]))
	i = i+1
	activeSensorArray.append([])

print 'hello'
print  activeSensorArray
'''
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
'''
print activeSensorArray
print data_store

print json_data
'''




