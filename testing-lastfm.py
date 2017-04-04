
from __future__ import division
import json
import pprint
import random
import math
import sys
from datetime import datetime
from geojson import Point
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.nostalgia


with open('akamediasystem.ldjson') as lastfm:
	songsObj = json.load(lastfm)

print "processed lastfm, google next"
print len(songsObj)
result = db.songs.insert_many(songsObj)
print result.inserted_ids

with open('LocationHistory.json') as locationHistory:
	locations = json.load(locationHistory)

result2 = db.locations.insert_many(locations['locations'])
print result2.inserted_ids
print "processed google raw intake"

# now crunch through each location entry and reformat for geojson. point is stored in key 'gj'
for u in db.locations.find().skip(3):
        newLat = u['latitudeE7']/10000000
        newLon = u['longitudeE7']/10000000
        np = Point((newLon,newLat))
        # print np
        idd = u['_id']
        db.locations.update({"_id":idd},{"$set":{"gj":np}, "$unset":{"latitudeE7": "" , "longitudeE7" :""}})


'''
sizeL = len(locations['locations'])
for i in range(10,-1,-1):
	index = random.randint(0,sizeL)
	print locations['locations'][index]
	# sample output:
	# {u'latitudeE7': 406805268, u'accuracy': 69, u'longitudeE7': -739619729, u'timestampMs': u'1376857779167'}
	# but also:
	# {u'activitys': [{u'activities': [{u'confidence': 100, u'type': u'tilting'}], u'timestampMs': u'1394494209396'}], u'latitudeE7': 407151972, u'accuracy': 91, u'longitudeE7': -739600297, u'timestampMs': u'1394494240827'}
	print ''

	'''