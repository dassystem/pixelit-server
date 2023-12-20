#!/usr/bin/python3
# -*- coding: utf-8 -*-

# INFOS SEE
#
# https://www.reddit.com/r/jellyfin/comments/locqof/jellyfin_api_current_playbacks/
# https://fra1.mirror.jellyfin.org/releases/openapi/stable/jellyfin-openapi-10.7.7.json
# https://github.com/MediaBrowser/Emby/wiki/Api-Key-Authentication
# # # #

import requests

# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config



sendheaders = {'Content-Type': 'application/json',
               'accept': 'application/json',
               'x-emby-token': config.jellyfin['apikey'],
               }

def getInfo(devices):
    currently_playing = []
    for device in devices.json():
        # Filter only devices that are currently playing something
        if device.get('NowPlayingItem'):
            currently_playing.append(device)
            #  Handle mutliple users use the service. Track the correct user
            try:
                currently_playing[0]['UserName'] == config.jellyfin['user']
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
                # on first match, leave cycling through devices
                break
            except: 
                print("[DEBUG] No device playing for user",config.jellyfin['user'])
    if not currently_playing:
        print("[DEBUG] No device playing.")
        pixelit.skipApp()

# Check for devices that have checked in in the last 90 seconds
#check if jellyfin is reachable / check for status 200
try:
    if requests.get(config.jellyfin['url']).status_code == 200:
        #print("Returncode is 200")
        devices = requests.get(
            config.jellyfin['url'] +
            '/Sessions?ActiveWithinSeconds=90',
            headers=sendheaders)
        getInfo(devices)
except:
    print("[ERROR] No connection to Jellyfin server under",config.jellyfin['url'])
    pixelit.skipApp()
    


