
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
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import akacreds
import os

# credential copt to local env vars
for t in akacreds.creds:
	os.environ[t] = akacreds.creds[t]
	print t, akacreds.creds[t]

client = MongoClient()
db = client.nostalgia
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

'''
for each unique song in db/songs, search spotify API for trackname + artist
if no artist name or no track name, ignore (and possibly remove entirely from db.songs?)
'''

songCursor = db.songs.find('gj':{'$exists':True}).limit(4)
for sng in songCursor:
	tt = sng['timestamp']
	print tt
	# nl = db.locations.find()
