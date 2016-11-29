import json
import time
import os
import subprocess
from pymongo import MongoClient
from bson.json_util import dumps
import StringIO
import sys
import ConfigParser
from urllib2 import urlopen
import ccnlite.client

def getConfig():


    print "Reading config file..."
    Config = ConfigParser.ConfigParser()
    Config.read('config.ini')

    global SENSOR_LIST_PREFIX
    global CCN_SUITE
    global SDS_IP
    global DATABASE_IP
    global DATABASE_PORT
    global SDS_PORT
    global LOCALHOST_IP
    global LOCALHOST_PORT



    SDS_IP = Config.get("INFO", 'SDS_IP')
    SDS_PORT = Config.get("INFO", 'SDS_PORT')


    SENSOR_LIST_PREFIX = Config.get("SENSORS", 'SENSOR_LIST_PREFIX')
    CCN_SUITE = Config.get("CCN", 'CCN_SUITE')
    DATABASE_IP = Config.get('DATABASE', 'DATABASE_IP') 
    DATABASE_PORT = Config.get("DATABASE", 'DATABASE_PORT')

    LOCALHOST_IP = Config.get("LOCALHOST", 'LOCALHOST_IP')
    LOCALHOST_PORT = Config.get("LOCALHOST", 'LOCALHOST_PORT')

def getSensorLists():
    process = os.popen("$CCNL_HOME/bin/ccn-lite-peek -s " + CCN_SUITE + " -u " + SDS_IP + "/" + SDS_PORT + " " + SENSOR_LIST_PREFIX + " | $CCNL_HOME/bin/ccn-lite-pktdump -f 2")
    sds_result = process.read() 
    print sds_result

    #sds_result = '[{"looptime": "5", "prefix": "/p/4b498c82/regist/foobar", "sensor_type": "Celsius", "location": "foobar", "time": "2016-11-24-15-47-49", "sensor_mac": "00:12:4b:49:8c:82", "_id": {"$oid": "5836fd9fd914e331492b046e"}, "sensor_model": "TI CC2650 SensorTag", "unit": "Lux", "sqn": "1"}, {"looptime": "5", "prefix": "/p/4b498c82/regist/utn", "sensor_type": "Celsius", "location": "UTN", "time": "2016-11-24-15-47-49", "sensor_mac": "00:12:4b:49:8c:82", "_id": {"$oid": "5836fd9fd914e331492b046f"}, "sensor_model": "TI CC2650 SensorTag", "unit": "Lux", "sqn": "1"}]'
    sds_json = json.loads(sds_result)
    sensor_array = []

    for sensor in sds_json:
        location = sensor['location']
        prefix = sensor['prefix']
        sensorMac = sensor['sensor_mac']
        time = sensor['time']
        initialSeqno = sensor['sqn']
        loopTime = sensor['looptime']
        sensor_array.append((location, prefix, sensorMac, time, initialSeqno, loopTime))

    return sensor_array

def dbSetup():
    global DATABASE
    client = MongoClient(DATABASE_IP+":"+DATABASE_PORT, serverSelectionTimeoutMS=3000)
    try:
        client.server_info()
    except:
        print "Couldn't connect to sensor database, exiting"
        sys.exit()
    print "Connected to database! ("+DATABASE_IP+":"+DATABASE_PORT+")"
    #db = client.test.sensorsdata
    #collection = db.sensorsdata
    DATABASE = client.test.sensorsdata

def peekSensors(sensor_array):

    for sensor in sensor_array:
        prefix =  sensor[1]

        #TODO update using sequence number

        process = os.popen("$CCNL_HOME/bin/ccn-lite-peek -s " + CCN_SUITE + " -u " + LOCALHOST_IP + "/" + LOCALHOST_PORT + " " + prefix + " | $CCNL_HOME/bin/ccn-lite-pktdump -f 2")
        #print("$CCNL_HOME/bin/ccn-lite-peek -s " + CCN_SUITE + " -u " + LOCALHOST_IP + "/" + LOCALHOST_PORT + " " + prefix + " | $CCNL_HOME/bin/ccn-lite-pktdump -f 2")
        sensor_result = process.read()
        print sensor_result    
        if(len(sensor_result) > 0):
            #search if in  DB
            tokens = sensor_result.split("-")
            seqno = tokens[0]
            #print("seqno: " + tokens[0])
            #print(sensor_result)
            cursor = DATABASE.find({"prefix": prefix+seqno})
            
            if cursor.count()==0:
                #content object not in DB
                result = DATABASE.insert_one({"prefix" : prefix+seqno, "value": sensor_result })
                print result
            else:
                print "***Error content object already in DB"
            #TODO: USE SEQUENCE NUMBER
            #seq_no = seq_no +1
        else:
            print("***Error NO SENSOR RESULT")

#def ConvertToSML():




def main():
    
    getConfig()
    sensor_array = getSensorLists()
    dbSetup()
    while True:
        if (sensor_array):
            peekSensors(sensor_array)
            time.sleep(5)
        
if __name__ == "__main__":
   main()