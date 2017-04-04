fewer last.fm than there are google loc history plays
most last.fm are from times when i'm at a desktop/at work/at home
so, chunk by days in order to spread out the day's songs over the day's travels

INPUT:
google location history (from google takeout)
last.fm song-playing history (from https://github.com/maxkueng/lastfmexport) export tool

OUTPUT:
a syncwalk representing the month's songs-and-travels

mongoDB structure:

collection SONGS:
	timestamp
	title
	artist
	album
	trackMBID
	artistMBID
	albumMBID

collection LOCATION:
	timestamp
	latitude
	longitude
	accuracy


for each song in last.fm dataset:
	* find the closest timestamp from google location history
		if the timestamp is from a month where there's no Nostalgia-Sonder syncwalk, create one
		if that timestamp already has a Feature attached to it:
			* add the song to the Feature's playlist
		else:
			* create a Feature (with no polygon-region yet) and add this song to the Feature's playlist
upon processing of all songs in last.fm dataset:
	For each Nostalgia-sonder:
		collect the coordinates of all Features
		generate voronoi triangulation of all features, and for each point append the polygon created by the triangulation
		