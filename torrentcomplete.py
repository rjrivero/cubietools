#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# Called when a torrent is complete
# Does not receive a single parameter from transmission -
# got to do our best to figure which torrent it has
# finished downloading.

# See http://subliminal.readthedocs.org/en/latest/
# See https://github.com/Diaoul/subliminal

from __future__ import unicode_literals
from babelfish import Language
from datetime import timedelta
import os.path
import subliminal

# Folder to scan for torrents
TORRENT_FOLDER = "/tank/torrent"
# subliminal cache file
REGION_CACHE = "/tmp/dogpile.cache.dbm"

# configure the cache
subliminal.region.configure('dogpile.cache.dbm', 
    arguments={ 'filename': REGION_CACHE })

# scan for videos in the folder and their subtitles
videos = subliminal.scan_videos(
             TORRENT_FOLDER,
             subtitles=False,
             embedded_subtitles=False
)

# Download subtitles if not already downloaded
for video in (v for v in videos if v.age < timedelta(days=1)):
    srt = os.path.splitext(video.name)[0] + ".srt"
    if not os.path.exists(srt):
        subs = subliminal.download_best_subtitles([video], {Language('eng')})
        for v, s in subs.iteritems():
            subliminal.save_subtitles(v, s, single=True)
