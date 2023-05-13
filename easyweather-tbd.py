#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests
import awtrix

import config
from datetime import date
from datetime import datetime
import time
from datetime import timedelta

import asyncio
import sys
import os

import pickle

merkurbotpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/matrix-bot"
sys.path.append(merkurbotpath)
import merkurbot


tempfile="yesterdaysweather.txt"

def writeWeatherToFile(weather):
  file=open(tempfile,"wb")
  pickle.dump(weather,file)
  file.close()

def readWeatherFromFile():
  file=open(tempfile,"rb")
  out=pickle.load(file)
  file.close()
  return out



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
    print("[Debug]",out)
    return out



def getWeatherObjects():  
  today = date.today()
  yesterday = today - timedelta(days = 1)
  
  print("[DEBUG] Today's date is: ", today)
  print("[DEBUG] Yesterday was: ", yesterday)

  url_today = "https://api.openweathermap.org/data/2.5/onecall?lat=51.17&lon=7.01&exclude=current,minutely,hourly,alerts&appid=3d4336a2efb5e7e9fdaaaa112f4cfea0&units=metric"
  unix_yesterday= yesterday.strftime("%s")

  url_yesterday = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=51.17&lon=7.01&appid=3d4336a2efb5e7e9fdaaaa112f4cfea0&units=metric&only_current={true}&dt="+unix_yesterday

  # Get weather objects
  weatherdata_today=weatherObject(today,getWeatherData(url_today))
  weatherdata_yesterday=readWeatherFromFile()
  
  if weatherdata_yesterday.getDate() < weatherdata_today.getDate():
    print("[DEBUG]",weatherdata_yesterday.getDate(), "is smaller than today",weatherdata_today.getDate())
    writeWeatherToFile(weatherdata_today)
    # if yesterday is really the day before, than save todays data for tomorrow
  else:
    print("[DEBUG]",weatherdata_yesterday.getDate(), "is bigger or equal than today", weatherdata_today.getDate())
  weatherdata_today.getTemp()
  
  return weatherdata_today, weatherdata_yesterday



def calcDiff(weatherdata_today,weatherdata_yesterday):
  c="°C"
  
  tempToday = weatherdata_today.getTemp()
  dateToday = weatherdata_today.getDate()
  tempYesterday = weatherdata_yesterday.getTemp()
  dateYesterday = weatherdata_yesterday.getDate()

  print("[INFO]","Heute:   ("+str(dateToday)+")"      ,tempToday,c)
  print("[INFO]","Gestern: ("+str(dateYesterday)+")"  ,tempYesterday,c)
  change=round(tempToday-tempYesterday,2)
  print("[INFO] Veränderung:",change)

  if change >=0:
    vorzeichen = "+"
  else:
    vorzeichen = ""
  # return value only
  returnvalue = vorzeichen+str(abs(change))+c

  # return text
  if abs(change) <=2:
    if float(tempYesterday)<float(tempToday):
      returntext = "Es wird heute mit " + str(tempToday) + c + " kaum wärmer, als gestern ("+vorzeichen+str(change)+"°C)"
    else:
      returntext = "Es wird heute mit " + str(tempToday) + c + " kaum kälter, als gestern ("+vorzeichen+str(change)+"°C)"
  elif abs(change) <=4:
    if float(tempYesterday)<float(tempToday):
      returntext = "Es wird heute mit " + str(tempToday) + c + " etwas wärmer, als gestern ("+vorzeichen+str(change)+"°C)"
    else:
      returntext = "Es wird heute mit " + str(tempToday) + c + " etwas kälter, als gestern ("+vorzeichen+str(change)+"°C)"
  elif abs(change) <=6:
    if float(tempYesterday)<float(tempToday):
      returntext = "Es wird heute mit " + str(tempToday) + c + " deutlich wärmer, als gestern ("+vorzeichen+str(change)+"°C)"
    else:
      returntext = "Es wird heute mit " + str(tempToday) + c + " deutlich kälter, als gestern ("+vorzeichen+str(change)+"°C)"
  else:
    if float(tempYesterday)<float(tempToday):
      returntext = "Es wird heute mit " + str(tempToday) + c + " krass wärmer, als gestern ("+vorzeichen+str(change)+"°C)"
    else:
      returntext = "Es wird heute mit " + str(tempToday) + c + " krass kälter, als gestern ("+vorzeichen+str(change)+"°C)"

  return returnvalue, returntext

def weather2matrixbot(msg):
    print("[INFO] Sending to Matrixbot:", msg)
    asyncio.get_event_loop().run_until_complete(merkurbot.sendText(msg))



if __name__ == "__main__":
  today, yesterday = getWeatherObjects()
  short, long = calcDiff(today,yesterday)
  awtrix.sendAwtrixApp("EasyWeather", short,red=255,green=255,blue=255,icon=1329,force="false",count=1,duration=0,repeat=1,id=11
    )
  weather2matrixbot(long)

    
