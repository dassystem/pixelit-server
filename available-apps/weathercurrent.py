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
    print("hot")
  elif temp > 20:
    print("warm")
  elif temp > 10:
    prin ("fresh")
  elif temp > 5:
    print("cold")
  elif temp > 0:
    print("frosty")
  elif temp > -5:
    print("icy")
  else:
    print("apokalyptic")
      

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

  getImage(currenttemp)
  print("[INFO] Sending ",currenttemp)
  pixelit.sendApp(
    text_msg=currenttemp,
    red=255,
    green=255,
    blue=255,
    icon="[0,0,65251,65251,65251,65251,0,0,0,65251,65251,65251,65251,65251,65251,0,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,65251,0,65251,65251,65251,65251,65251,65251,0,0,0,65251,65251,65251,65251,0,0]",
     bigFont="false",
     scrollText='false',
     centerText="true"
  )

    
