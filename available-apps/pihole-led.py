#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests

# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config

# For V6 see: https://github.com/bazmonk/pihole6_exporter/blob/main/pihole6_exporter
# https://github.com/sbarbett/pihole6api <--- !

from pihole6api import PiHole6Client

def extract_key_value(json_data, key):
    """Extracts a specific key-value pair from a JSON data"""
    data = json.loads(json_data)
    value = data.get(key)
    return value

def getAdsBlockedToday():
  try: 
    client = PiHole6Client(config.pihole['url'], config.pihole['apitoken'])
    queries = client.metrics.get_stats_summary()
  #print(queries)
    totalblocked=queries['queries']['blocked']
    return str(totalblocked)
  except:
    print("[ERROR] Could not reach pi hole URL under", config.pihole['url'])
    pixelit.skipApp()
    quit()


def send2matrix(printtext): 
  print("[INFO] Sending to LED Matrix:",printtext)
  pixelit.sendApp(
    text_msg=printtext,
    red=255,
    green=255,
    blue=255,  
    icon="[0,0,4000,4000,0,4000,0,0,0,0,0,4000,4000,0,0,0,0,0,63488,63488,36864,36864,0,0,0,63488,63488,63488,63488,36864,36864,0,0,63488,36864,0,0,36864,36864,0,0,36864,36864,0,0,36864,63488,0,0,36864,36864,63488,63488,63488,63488,0,0,0,36864,36864,63488,63488,0,0]",
    bigFont="false",
    scrollText="auto", 
    centerText="true",
    )


if __name__ == "__main__":
  myappname="pihole"

  data=getAdsBlockedToday()
  pixelit.writeDataToFile(data,myappname)

#  if pixelit.exceedsTimeLimit(myappname,config.pihole['fetchEveryMinutes']):
#    data=getAdsBlockedToday()
#    pixelit.writeDataToFile(data,myappname)
#  else:
#    try:
#      data=pixelit.readDataFromFile(myappname)
#    except:
#      data=getAdsBlockedToday()
#      pixelit.writeDataToFile(data,myappname)
  send2matrix(data)
  
