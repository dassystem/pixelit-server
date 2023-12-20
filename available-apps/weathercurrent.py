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
    out=self.data['daily'][0]['temp']['day']
    out=round(out,1)
    return out



def getWeatherObjects():  
  today = date.today()

  lat = str(config.weather['lat'])
  lon = str(config.weather['lon'])
  appid = str(config.weather['apikey'])

  url_today = "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&exclude=current,minutely,hourly,alerts&appid="+appid+"&units=metric"
  
    # Get weather objects
  weatherdata_today=weatherObject(today,getWeatherData(url_today))
  weatherdata_today.getTemp()
  
  return weatherdata_today

if __name__ == "__main__":
  myappname="weather"
  if pixelit.exceedsTimeLimit(myappname,config.weather['fechtEveryMinutes']):
    currenttemp = str(getWeatherObjects().getTemp())+"°C"
    pixelit.writeDataToFile(currenttemp,myappname)
  else:
    try:
      currenttemp=pixelit.readDataFromFile(myappname)
    except:
      currenttemp = str(getWeatherObjects().getTemp())+"°C"
      pixelit.writeDataToFile(currenttemp,myappname)
  
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

    
