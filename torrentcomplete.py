#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# Called when a torrent is complete
# Does not receive a single parameter from transmission -
# got to do our best to figure which torrent it has
# finished downloading.

# See http://subliminal.readthedocs.org/en/latest/
# See https://github.com/Diaoul/subliminal

from __future__ import unicode_literals
from babelfish import Language
from datetime import timedelta
import subliminal

# Folder to scan for torrents
TORRENT_FOLDER = "/tank/torrent"
# subliminal cache file
REGION_CACHE = "/tmp/dogpile.cache.dbm"

# configure the cache
subliminal.cache_region.configure('dogpile.cache.dbm', 
	arguments={ 'filename': REGION_CACHE })

# scan for videos in the folder and their subtitles
videos = subliminal.scan_videos(
	[TORRENT_FOLDER],
	subtitles=True,
	embedded_subtitles=True,
	age=timedelta(days=1)
)

# Get the full path of each video
paths = tuple(video.name for video in videos)

# download
subliminal.download_best_subtitles(
	videos,
	{Language('eng'),}
)

# Rename the subtitles file to match the video name exactly
from os.path import join, splitext, basename, dirname
from os import rename
from shutil import copyfile
for path in paths:
	dname = dirname(path)
	bname = basename(path)
	video = splitext(bname)[0]
	try:
		copyfile( join(dname, "%s.en.srt" % video),
			join(dname, "%s.srt" % video))
	except:
		pass
