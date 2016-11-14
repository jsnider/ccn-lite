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
from subprocess import call
import ccnlite.client
nw = ccnlite.client.Access()

projectPrefixString = "unoise"
locPrefixArray = ['utn','foobar', 'rullan']
nodePrefixArray = ['node1', 'node2']
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
	for node in nodePrefixArray:
		for seqno in seqnoPrefixArray:
			currPrefix = '/'+ projectPrefixString +'/'+ location +'/'+ node +'/' + seqno
			#print currPrefix
			pkts = nw.getLabeledContent(currPrefix, raw=False) #TODO if this doesn't return anything the program breaks add a check
			#print pkts[0]
			#print 'j: ' + str(j)
			#print 'i: ' + str(i)
			#print data_store
			data_store[i][j].append(pkts[0].rstrip('\r\n'))
		j = j+1
		data_store[i].append([])
	i = i+1
	data_store.append([[]])

print data_store #TODO store this in a database
# this data object is gross becasue it marks the end of every array with an empty array
# but the output is [[location1:[node1_list], [node2_list], []], [location2:[node1_list], [node2_list], []], [location3:[node1_list], [node2_list], []], [[]]]
# example output [[['90', '60', '40', '20'], ['85', '65', '45', '15'], []], [['45', '50', '60', '70'], ['43', '52', '63', '69'], []], [['200', '250', '300', '400'], ['180', '275', '280', '420'], []], [[]]]

#build sensor data string
i=0 #for location
j=0 #for node
activeSensorString = ''

for location in locPrefixArray:
	activeSensorString = activeSensorString + location + ':'
	j=0
	for node in nodePrefixArray:
		if (int(data_store[i][j][0]) >= 0): #if the data_store array has a value for a node then the node is alive typ
			#print node + ' is active' 
			activeSensorString = activeSensorString + node + ','
			#print '*** string ***'
			#print activeSensorString
		j = j+1
print activeSensorString 
# TODO maybe make a json object out of this
# this string is gross because each end has an extra comma at the end
# example output: utn:node1,node2,foobar:node1,node2,rullan:node1,node2,


#write the string to a txt file
f = open('activeSensorString.txt', 'w')
f.write(activeSensorString + '\n')
f.close()

#use the subprocess command with the text file you just made 
call("/home/josn3503/ccn-lite/bin/ccn-lite-mkC -i /home/josn3503/ccn-lite/src/py/activeSensorString.txt -s ndn2013 '/ndn/test/activeSensorString' > /home/josn3503/ccn-lite/test/ndntlv/activeSensorString.ndntlv", shell=True)

#add content object file to cache
call("$CCNL_HOME/bin/ccn-lite-ctrl -x /tmp/mgmt-relay-b.sock addContentToCache $CCNL_HOME/test/ndntlv/activeSensorString.ndntlv", shell=True)

pkts = nw.getLabeledContent('/ndn/test/activeSensorString', raw=False)
print pkts[0]

#TODO: store values in data base

#TODO: do prediction stuff and make content objects




