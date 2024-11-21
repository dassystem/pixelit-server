#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests

# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config


def getOpenDotaData():
  sendheaders = {'Content-Type': 'application/json'}
  playerwin= 'https://api.opendota.com/api/players/'+str(config.dota['player'])+'/wl?date='+str(config.dota['days'])+'&game_mode='+str(config.dota['gamemode'])
  try:
    windata = requests.get(url=playerwin,headers=sendheaders)
    return(windata)
  except: 
    print("[Error] Cannot connect to opendota")
    pixelit.skipApp()
    quit()

def getAllOpenDotaData():
  sendheaders = {'Content-Type': 'application/json'}
  playerwin= 'https://api.opendota.com/api/players/'+str(config.dota['player'])+'/matches?date='+str(config.dota['days'])
  try:
    windata = requests.get(url=playerwin,headers=sendheaders)
    return(windata)
  except: 
    print("[Error] Cannot connect to opendota")
    pixelit.skipApp()
    quit()


def calcWinrate(windata):
  mywindata = json.loads(json.dumps(windata.json()))
  print(mywindata)
  win=mywindata['win']
  lose=mywindata['lose']

  if win+lose == 0:
    printtext = "0 Games"
  else:
    winrate = round(float(win)/(int(lose)+int(win)),3)*100
    printtext= str(round(winrate,2)) +'%'
  return(printtext)


def showWinrate(printtext): 
  print("[INFO] Sending to LED Matrix:",printtext)
  pixelit.sendApp(
    text_msg=printtext,
    red=255,
    green=255,
    blue=255,  
    icon="[43008,43008,43008,43008,43008,43008,43008,43008,43008,0,43008,43008,43008,0,0,43008,43008,43008,0,0,43008,43008,0,43008,43008,43008,0,0,0,43008,43008,43008,43008,43008,43008,0,0,0,43008,43008,43008,0,43008,43008,0,0,0,43008,43008,0,0,43008,43008,0,0,43008,43008,43008,43008,43008,43008,43008,43008,43008]",
    bigFont="false",
    scrollText="auto", 
    centerText="true",
    )

if __name__ == "__main__":
  myappname="dota"
  
  if pixelit.exceedsTimeLimit(myappname,config.dota['fetchEveryMinutes']):
    data=calcWinrate(getOpenDotaData())
    pixelit.writeDataToFile(data,myappname)
  else:
    try:
      data=pixelit.readDataFromFile(myappname)
    except:
      data=calcWinrate(getOpenDotaData())
      pixelit.writeDataToFile(data,myappname)
  showWinrate(data)

  # TODO: Create class PlayerProfile and get all relevant data on creation via OpenDota

