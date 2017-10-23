#!/usr/bin/python
from deluge_framework import filter_torrents
def torrentAction(torrent_id,torrent_info):
    print ('%s: %s %s' % (torrent_id,torrent_info['state'],torrent_info['progress']))
    return ''
filter_torrents({},['name','state','progress'],torrentAction)
