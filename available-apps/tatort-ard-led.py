#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import datetime
from datetime import date
from bs4 import BeautifulSoup
import logging


# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config



def scrapHTML(myurl):
    rawdata = requests.get(myurl)
    html = rawdata.content
    soup = BeautifulSoup(html, 'html.parser')
    # get sendetermine-2019-wochentag
    return soup.find_all(
        True, {'class': ['topTeaser']})

def sortByDate(data):
    return data['date']



def krimi2ledmatrix(msg):
    print("[INFO] Sending to ledmatrix:", msg)
    #has fresh tatort 
    myicon="[693,693,65535,693,693,693,693,693,65535,65535,65535,65535,65535,693,693,693,693,693,65535,693,693,65535,693,693,693,65535,65535,65535,693,693,65535,693,65535,693,65535,693,65535,693,693,65535,693,693,65535,693,693,65535,693,65535,65535,65535,693,65535,65535,65535,65535,65535,693,693,65535,693,693,65535,693,65535]"
    pixelit.sendApp(text_msg=msg,
                    red=255,
                    green=255,
                    blue=255,
                    icon=myicon,
                    bigFont="false",
                    scrollText="auto",
                    centerText="false",
                    )

def checktatort():
    #TODO: Get tatort / polizeiruf series. Need to check the headline class_: 'conHeadline' and search for "Tatort" or "Polizeiruf: 110"
    tatorturl="https://www.daserste.de/unterhaltung/krimi/tatort/vorschau/index.html"
    rawhtml = scrapHTML(tatorturl)
    nextDate = getTatortdate(rawhtml)
    #print("Date:", nextDate)
    nextTitle= getTatorttitle(rawhtml)
    #print("Title:", nextTitle)
    nextSeriesName=getSeriesname(rawhtml)
    return nextSeriesName, nextTitle, nextDate


def getTatortdate(html):
    for onAir in html:
        tatortdate=onAir.find(class_='dachzeile')
        tatortdate = BeautifulSoup(str(tatortdate),'html.parser')
        tatortdate = tatortdate.text.strip()
    return tatortdate
    
def getTatorttitle(html):
    for onAir in html:
        tatorttitle=onAir.find(class_='headline')
        tatorttitle = BeautifulSoup(str(tatorttitle),'html.parser')
        tatorttitle = tatorttitle.text.strip()
    return tatorttitle   

def getSeriesname(html):
    seriesName=""
    for onAir in html:
        seriesName =onAir.find(class_='conHeadline')
        seriesName =BeautifulSoup(str(seriesName),'html.parser')
        seriesName = seriesName.text.strip()
        #print(seriesName)

    if seriesName.find("Polizeiruf") !=-1:
      #print("Polizeiruf")
      return "Polizeiruf"
    elif seriesName.find("Tatort") !=-1:
      #print("Tatort")
      return "Tatort"
    else:
      print("[ERROR] KEIN SERIENNAME GEFUNDEN!")
      return "KEIN SERIENNAME GEFUNDEN"   

if __name__ == "__main__":
    myappname="tatortARD"

    if pixelit.exceedsTimeLimit(myappname,config.tatort['fechtEveryMinutes']):
        mySeries,myTitle,myTime = checktatort()
        msg ="Nächster "+ str(mySeries) + ": »" + str(myTitle) + "« am " + str(myTime)
        krimi2ledmatrix(msg)
    else:
      try:
        data=pixelit.readDataFromFile(myappname)
      except:
        mySeries,myTitle,myTime = checktatort()
        msg ="Nächster "+ str(mySeries) + ": »" + str(myTitle) + "« am " + str(myTime)
        krimi2ledmatrix(msg)

    