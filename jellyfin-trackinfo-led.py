#!/usr/bin/python3
# -*- coding: utf-8 -*-

# INFOS SEE
#
# https://www.reddit.com/r/jellyfin/comments/locqof/jellyfin_api_current_playbacks/
# https://fra1.mirror.jellyfin.org/releases/openapi/stable/jellyfin-openapi-10.7.7.json
# https://github.com/MediaBrowser/Emby/wiki/Api-Key-Authentication
# # # #

import requests
import pixelit
import config

sendheaders = {'Content-Type': 'application/json',
               'accept': 'application/json',
               'x-emby-token': config.jellyfin['apikey'],
               }

# TODO: Build try catch 
    # if jellyfin is not reachable.
    # then skip the entire app (instead of crashing)

# Check for devices that have checked in in the last 90 seconds
devices = requests.get(
    config.jellyfin['url'] +
    '/Sessions?ActiveWithinSeconds=90',
    headers=sendheaders)
currently_playing = []

for device in devices.json():
    # Filter only devices that are currently playing something
    if device.get('NowPlayingItem'):
        currently_playing.append(device)
        #  Handle mutliple users use the service. Track the correct user
        if(currently_playing[0]['UserName'] == config.jellyfin['user']):
            print("[INFO] user", config.jellyfin['user'], "detected")
            track = currently_playing[0]['NowPlayingItem']['Name']
            artist = currently_playing[0]['NowPlayingItem']['Artists'][0]
            mytext = "Now playing »" + track + "« by " + artist

        # Send track-info to LED-Matrix
            print("[INFO]", mytext)
            pixelit.sendApp(
                text_msg=mytext,
                red=255,
                green=255,
                blue=255,
                icon="[0,0,0,0,0,0,0,0,0,0,65535,65535,65535,65535,65535,0,0,0,65535,0,0,0,65535,0,0,0,65535,0,0,0,65535,0,0,0,65535,0,0,0,65535,0,0,65535,65535,0,0,65535,65535,0,0,65535,65535,0,0,65535,65535,0,0,0,0,0,0,0,0,0]",
                bigFont="false",
                scrollText="auto",
                centerText="false",
                )

if not currently_playing:
    print("[DEBUG] No device playing.")
    pixelit.skipApp()
