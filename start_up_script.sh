#!/bin/bash

PLAYLIST_DIR="/var/lib/mpd/playlists"
MEDIA_DIR="/home/ivo/media"

for dir in "$MEDIA_DIR"/*     # list directories in the form "/tmp/dirname/"
do
    dir=${dir%*/}      # remove the trailing "/"
    dir_name="${dir##*/}"    # print everything after the final "/"

    # Is it a directory?
    if [ -d "$dir" ]; then
      find $dir -type f -name \*.mp3 > "$PLAYLIST_DIR/$dir_name.m3u"
      echo "$dir Playlist created ..."
    fi
done

sleep 10s

sudo /home/ivo/mood_light/virtenv/bin/python /home/ivo/mood_light/mood_lighting/start.py >> /home/ivo/mood_light/mood_light.log 2>&1
# sudo /home/ivo/mood_light/virtenv/bin/python start.py
