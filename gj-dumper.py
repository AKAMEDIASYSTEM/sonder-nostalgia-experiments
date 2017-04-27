
from __future__ import division
import json
import geojson
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


client = MongoClient()
db = client.nostalgia

r = db.syncwalks.find({}).limit(1)
for i in r:
	print i['gj']