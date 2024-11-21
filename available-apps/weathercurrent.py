#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests

from datetime import date

# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config

def getWeatherData(myurl):
  # URLs
  sendheaders = {'Accept': 'application/json'}
  weatherData = json.loads(json.dumps(requests.get(url=myurl, headers=sendheaders).json()))
  return(weatherData)

class weatherObject:

  def __init__(self, date, jsonData):
    self.data = jsonData
    self.date = date

  def getData(self):
    return self.data

  def getDate(self):
    return self.date

  def getTemp(self):
    #print(self.data)
    out=self.data['main']['temp']
    out=round(out,1)
    #print("temperatur ist", out)
    return out



def getWeatherObjects():  
  today = date.today()

  lat = str(config.weather['lat'])
  lon = str(config.weather['lon'])
  appid = str(config.weather['apikey'])

  url_today =  "https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&exclude=current,minutely,hourly,alerts&appid="+appid+"&units=metric"
  try:
    # Get weather objects
    weatherdata_today=weatherObject(today,getWeatherData(url_today))
    weatherdata_today.getTemp()
    return weatherdata_today
  except:
    print("[ERROR] Not connecting to openweathermap or parsing errors")
    pixelit.skipApp()
    quit()

def getImage(temp):
  temp = float(temp[:-2])
  if temp > 30:
    #print("hot")
    icon="[0,0,0,59392,0,0,0,0,0,0,0,59392,0,0,0,0,0,0,59392,60672,0,59392,0,0,0,59392,59392,60672,59392,60672,59392,0,59392,60672,59392,65312,60672,60672,59392,59392,59392,60672,65312,65459,65459,65312,60672,59392,59392,60672,65312,65459,65459,65312,60672,59392,0,59392,60672,65312,65312,60672,59392,0]"
#    icon="[0,0,65504,0,0,65504,0,0,0,0,0,0,0,0,0,0,65504,0,0,65504,65504,0,0,65504,0,0,65504,65504,65504,65504,0,0,0,0,65504,65504,65504,65504,0,0,65504,0,0,65504,65504,0,0,65504,0,0,0,0,0,0,0,0,0,0,65504,0,0,65504,0,0]"
  elif temp > 18:
    #print("warm")
    icon="[0,0,0,0,0,44373,65535,0,0,65535,65535,0,44373,65535,65535,44373,44373,65535,65535,0,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,0,44373,65535,65535,65535,65535,1119,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]"
  elif temp > 10:
    #print("fresh")
    icon="[0,0,0,0,0,0,0,0,0,0,0,0,0,46486,46486,0,0,0,0,46486,46486,65535,65535,46486,0,0,46486,65535,65535,65535,65535,46486,0,0,46486,65535,65535,65535,65535,46486,0,46486,46486,46486,46486,46486,46486,46486,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]"
  elif temp > 5:
    #print("cold")
    icon="[0,0,0,0,0,44373,65535,0,0,65535,65535,0,44373,65535,65535,44373,44373,65535,65535,0,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,0,44373,65535,65535,65535,65535,1119,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]"
  elif temp > 0:
    #print("frosty")
    icon="[0,0,0,53247,0,0,0,0,0,53247,0,53247,0,53247,0,0,0,0,53247,53247,53247,0,0,0,53247,53247,53247,0,53247,53247,53247,0,0,0,53247,53247,53247,0,0,0,0,53247,0,53247,0,53247,0,0,0,0,0,53247,0,0,0,0,0,0,0,0,0,0,0,0]"
  elif temp > -5:
    #print("icy")
    icon="[0,0,0,53247,0,0,0,0,0,53247,0,53247,0,53247,0,0,0,0,53247,53247,53247,0,0,0,53247,53247,53247,0,53247,53247,53247,0,0,0,53247,53247,53247,0,0,0,0,53247,0,53247,0,53247,0,0,0,0,0,53247,0,0,0,0,0,0,0,0,0,0,0,0]"
  else:
    #print("apokalyptic")
    icon="[0,0,0,0]"
  return icon
      

if __name__ == "__main__":
  myappname="weather"
  if pixelit.exceedsTimeLimit(myappname,config.weather['fechtEveryMinutes']):
    currenttemp = str(getWeatherObjects().getTemp())+"°C"
    pixelit.writeDataToFile(currenttemp,myappname)
  else:
    try:
      # load from cache
      currenttemp=pixelit.readDataFromFile(myappname)
    except:
      # if not loading, try grab fresh info
      currenttemp = str(getWeatherObjects().getTemp())+"°C"
      pixelit.writeDataToFile(currenttemp,myappname)

  #getImage(currenttemp)
  print("[INFO] Sending ",currenttemp)
  pixelit.sendApp(
    text_msg=currenttemp,
    red=255,
    green=255,
    blue=255,
    icon=getImage(currenttemp),
    bigFont="false",
    scrollText='false',
    centerText="true"
  )

    
