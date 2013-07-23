'''
Created on Apr 28, 2013

@author: sriram
'''
import urllib, json
import pprint
origin = "london"
destination = "southampton"
URL2 = "http://maps.googleapis.com/maps/api/directions/json?origin=Boston,MA&destination=Concord,MA&waypoints=Charlestown,MA|Lexington,MA&sensor=false"
# URL2 = "http://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=false"

googleResponse = urllib.urlopen(URL2)
jsonResponse = json.loads(googleResponse.read())
# print jsonResponse['routes']
route = jsonResponse['routes'][0]
print route
# pprint.pprint(jsonResponse)
# 
# 
# test = json.dumps([s['geometry']['location'] for s in jsonResponse['results']], indent=3)
# data  = json.loads(test)
# print(data)