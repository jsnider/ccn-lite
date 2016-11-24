#peek a router

#check to see if in database by sequence number

#
from pymongo import MongoClient
import time
import json


import ccnlite.client
nw = ccnlite.client.Access()
nw.connect("127.0.0.1", 9999)
#pkts = nw.getLabeledContent("/unoise/foobar/node2/3", raw=False)
#print pkts[0]

#TODO: test connection if fails then exit

### GET SENSOR INFO FROM SDS
sds = ccnlite.client.Access()
sds.connect("130.238.15.229", 9999)
pkts = nw.getLabeledContent("/sds/sensors", raw=False)
print pkts[0]

sds_result = '[{"looptime": "5", "prefix": "/p/4b498c82/regist/foobar", "sensor_type": "Celsius", "location": "foobar", "time": "2016-11-24-15-47-49", "sensor_mac": "00:12:4b:49:8c:82", "_id": {"$oid": "5836fd9fd914e331492b046e"}, "sensor_model": "TI CC2650 SensorTag", "unit": "Lux", "sqn": "1"}, {"looptime": "5", "prefix": "/p/4b498c82/regist/foobar", "sensor_type": "Celsius", "location": "foobar", "time": "2016-11-24-15-47-49", "sensor_mac": "00:12:4b:49:8c:82", "_id": {"$oid": "5836fd9fd914e331492b046f"}, "sensor_model": "TI CC2650 SensorTag", "unit": "Lux", "sqn": "1"}]"'

sds_json = json.dumps(pkts[0])

print sds_json


#$CCNL_HOME/bin/ccn-lite-peek -s ndn2013 -u 130.238.15.229/9999 "/sds/sensors"   | $CCNL_HOME/bin/ccn-lite-pktdump -f 2

'''

client = MongoClient()
db = client.project
db.live_data

seq_no = 1

while seq_no < 4:
	prefix = "/unoise/utn/node2/" + str(seq_no)
	pkts = nw.getLabeledContent(prefix, raw=False)
	#print pkts[0]
	
	#search if in  DB
	cursor = db.live_data.find({"prefix": prefix})
	
	if cursor.count()==0:
		#content object not in DB
		result = db.live_data.insert_one({"prefix" : prefix, "value": pkts[0] })
		print result
	else:
		print "***Error content object already in DB"
	time.sleep(2)
	seq_no = seq_no +1
'''