
# *****************************************************************************
# Copyright (c) 2016 IBM Corporation and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#   Lokesh Haralakatta
# *****************************************************************************

'''
    Example of retrieving a list of the first five documents from a database for
    the device "piCam-1", applying the view by-deviceId and further process the
    device data to get data values for the first five documents
'''
import requests

print "hello"

# Define cloudant username
user = "824ec716-c094-47ff-a4e0-dca7918f3e8c-bluemix"

# Define cloudant password
passwd = "f846902c4c121441f60ac3a844656038faece954cd913e33ea4bb6b3d51241a6"

# Define cloudant host
host = user+".cloudant.com"

# Define cloudant db name
db = "iotp_z0zqjv_default_2016-11"

# Define view variable to contain the Map View Name
view = "by-deviceId?limit=5"

# Frame the URL using above defned variables values
url = 'https://'+host+'/'+db+'/_design/iotp/_view/'+view

print "url"
print url

# Define args variable to store required parameter values
args = { 'key'  :  ' "Room345" '  ,  'limit'  :  '5'  }

# Invoke HTTP GET request with all required parameters
response = requests.get(url,params=args,auth=(user,passwd))

print "hi"

# Check the response status code, should be 200 to proceed further
if ( response.status_code == 200):
    print "200"
    # Get the response data in JSON format
    jsonData = response.json()
    # Get the device data records which are JSON array of rows with in jsonData
    records = jsonData['rows']

    print jsonData

    # For each record, get deviceType, deviceID and devicedata from the records
    for record in records:
        dType = record['value']['deviceType']
        dID = record['value']['deviceId']
        dValue = record['value']['data']['d']['temperature']
        print "Device Type: %s  Device Id: %s  Value: %s" %(dType,dID,str(dValue))
else:
    print "why"
    print "HTTP GET Failed with Status Code - %s" %(response.status_code)

print "bye"