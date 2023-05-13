#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests
import pixelit

import config


def getAdsBlockedToday():
  sendheaders = {'Content-Type': 'application/json'}
  piholeurl= config.pihole['url']+'/admin/api.php?summary&auth='+config.pihole['apitoken']
  #print("[DEBUG]" Pi-Hole URL:, piholeurl)

  piholedata = json.loads(requests.get(url=piholeurl,headers=sendheaders).content.decode("utf-8"))

  out=piholedata["ads_blocked_today"]
  out=out.replace(",", ".") #decimal comma
  return out



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

  if pixelit.exceedsTimeLimit(myappname,config.pihole['fechtEveryMinutes']):
    data=getAdsBlockedToday()
    pixelit.writeDataToFile(data,myappname)
  else:
    try:
      data=pixelit.readDataFromFile(myappname)
    except:
      data=getAdsBlockedToday()
      pixelit.writeDataToFile(data,myappname)
  send2matrix(data)
  
