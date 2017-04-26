
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

'''
for each unique song in db/songs, search spotify API for trackname + artist
if no artist name or no track name, ignore (and possibly remove entirely from db.songs?)
'''

# for t in akacreds.creds:
# 	os.environ[t] = akacreds.creds[t]
# 	print t, akacreds.creds[t]



client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
