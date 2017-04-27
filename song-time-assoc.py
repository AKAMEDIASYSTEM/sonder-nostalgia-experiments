
from __future__ import division
import json
import pprint
import random
import math
import sys
from datetime import datetime
from datetime import timedelta
from geojson import Point
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.nostalgia


for u in db.songs.find({"timestamp":{"$gt":datetime.fromtimestamp(1180639052)}}).skip(10000).limit(100):
        date1 = u['timestamp'] - timedelta(days=0.2)
        date2 = u['timestamp'] + timedelta(days=0.2)
        # NOTE, "ascending" is the sort-order we want if we want the closest entry first
        r = db.locations.find({"time":{"$gte":date1, "$lte":date2}}).sort("time",pymongo.ASCENDING).limit(1)
        # print '%i matches at %s'% (r, u['timestamp'])
        if r.count() is not 0:
                print r[0]['gj']
                qq = db.songs.update({'_id':u['_id']},{'$set':{'gj':r[0]['gj']}},False)
                print qq
                # update the song with the loc
                # print 'hey now, match at %s' % u['timestamp']
                # print result
                # print u['timestamp']-result['time']


'''
# for s in songs:
#    upsert (creating syncwalk AND songs[] array if necessary) song into new syncwalk, with name: "%B %Y"                
# 
# for s in db.songs.find({"timestamp":{"$gt":datetime.fromtimestamp(1180639052)}}).limit(10):
for s in db.songs.find():
        syncwalkName = s['timestamp'].strftime('%B %Y')
        upsertResult = db.syncwalks.update(
                {"name":syncwalkName},
                {"$push":{"songs":s}},
                True)

print upsertResult
print syncwalkName
'''
### NOTE, the above works pretty good, but we should FIRST try 
### to do a soptify-mbid reconciliation so the syncwalks have playable tracks
### ALSO this is premature, because each song in db.songs needs a temporally-nearest 
### location appended to it...




### HERE's where wel'll move all unique-MBID songs 


'''
# # do raw intake of lastfm and goog data
# with open('akamediasystem.ldjson') as lastfm:
# 	songsObj = json.load(lastfm)
# for song in songsObj:
#         if song['time'] == 0:
#                 print 'encountered timeless song'
#                 song['timestamp'] = datetime.fromtimestamp(1180639052)
#         else:
#                 timeraw = int(song['time']) / 1000.0
#                 song['timestamp'] = datetime.fromtimestamp(timeraw)
        # print song['timestamp']
# print songsObj

# print "processed lastfm, google next"
# print len(songsObj)
# result = db.songs.insert_many(songsObj)
# print result.inserted_ids

with open('LocationHistory.json') as locationHistory:
	locations = json.load(locationHistory)

result2 = db.locations.insert_many(locations['locations'])
print result2.inserted_ids
print "processed google raw intake"
'''

'''
# now crunch through each location entry and reformat for geojson. point is stored in key 'gj'
for u in db.locations.find().skip(3):
        newLat = u['latitudeE7']/10000000
        newLon = u['longitudeE7']/10000000
        np = Point((newLon,newLat))
        # print np
        idd = u['_id']
        db.locations.update({"_id":idd},{"$set":{"gj":np}, "$unset":{"latitudeE7": "" , "longitudeE7" :""}})
'''

'''
# normalize time format in goog dataset
for u in db.locations.find().skip(3):
        timeraw = int(u['timestampMs']) / 1000.0
        ti = datetime.fromtimestamp(timeraw)
        # print ti
        idd = u['_id']
        db.locations.update({"_id":idd},{"$set":{"time":ti}, "$unset":{"timestampMs": ""}})
'''

# for u in db.songs.find({"time":{"$ne":0}}):
#         print u['time']
#         timeraw = int(u['time'] / 1000.0)
#         ti = datetime.fromtimestamp(timeraw)
#         print ti
#         idd = u['_id']
#         db.songs.update({"_id":idd},{"$set":{"timestamp":ti}})

# for u in db.songs.find({"time":{"$type":"long"}}):
#         print u['time']
#         timeraw = int(u['time'] / 1000.0)
#         ti = datetime.fromtimestamp(timeraw)
#         print ti
#         idd = u['_id']
#         db.songs.update({"_id":idd},{"$set":{"timestamp":ti}})
# print 'done with timestamp update'

# print db.songs.findOne({"time":{"$gt":0}}) # this fails as "colleciton obj is not callable" but no matter, update worked

'''
for ss in db.songs.find({"time":{"$gt":0}}).skip(3).limit(3):
        songtime = ss['time']
        songu = songtime / 1000.0
        timecomp = datetime.fromtimestamp(songu)
        print timecomp
        locresult = db.locations.find({"time":{"$gte":timecomp}}).sort([("time",1)]).limit(1)
        locresult2 = db.locations.find({"time":{"$lte":timecomp}}).sort([("time",1)]).limit(1)
	# locresult = db.locations.find({"time":{"$gte":timecomp}}).limit(1)
        # locresult2 = db.locations.find({"time":{"$lte":timecomp}}).limit(1)
        for ress in locresult:
                print "gte result"
                print ress
        for resss in locresult2:
                print "lte result"
                print resss
print 'done'
'''

'''
how to get "february" out of a datetime:
g = datetime.datetime.now() # or w/e datetime
calendar.month_name[g.month]
--OR--
g.strftime('%B')
>>> g.strftime('%B %Y')
'April 2017'


'''