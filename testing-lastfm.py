
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

'''
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

for ss in db.songs.find({"time":{"$gt":0}}).limit(3):
	timeraw = ss['time'] / 1000.0
        ti = datetime.fromtimestamp(timeraw)
        # print ti
        locresult = db.locations.find({"timestampMS":{"$gte":ti,"$lte":ti}}).sort([{"timestampMS":1}]).limit(1)
	print locresult
