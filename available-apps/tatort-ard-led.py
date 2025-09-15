#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import datetime
#from datetime import datetime
from bs4 import BeautifulSoup
import logging
import locale


# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config

#locale.setlocale(locale.LC_TIME, locale.normalize("de"))

def scrapHTML(myurl):
    rawdata = requests.get(myurl)
    html = rawdata.content
    soup = BeautifulSoup(html, 'html.parser')
    # get sendetermine-2019-wochentag
    return soup.find_all(
        True, {'class': ['topTeaser']},limit=1) #stop after first encounter

def sortByDate(data):
    return data['date']

def dateConvert(oldDate):
    #In: Mo., 01.01. | 20:15 Uhr
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
    newDate=datetime.datetime.strptime(oldDate,'%a., %d.%m. | %H:%M Uhr')
    #print(type(newDate))
    #print(newDate)
    return newDate



def krimi2ledmatrix(msg,happens):
    print("[INFO] Sending to ledmatrix:", msg)
    #has fresh tatort 
    if happens == False:
        myicon="[693,693,65535,693,693,693,693,693,65535,63488,65535,65535,65535,693,693,63488,693,693,63488,693,693,65535,63488,693,693,65535,65535,63488,693,63488,65535,693,65535,693,65535,693,63488,693,693,65535,693,693,65535,63488,693,63488,693,65535,65535,65535,63488,65535,65535,65535,63488,65535,693,63488,65535,693,693,65535,693,63488]"
    else:
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

def checktatort(krimiurl):
    #Get tatort / polizeiruf series. Need to check the headline class_: 'conHeadline' and search for "Tatort" or "Polizeiruf: 110"
#    tatorturl=polizeirufurl
    try: 
      rawhtml = scrapHTML(krimiurl)
      #print("[DEBUG] testing",krimiurl)
      #print("scraped")
    except:
      print("[ERROR] ARD URL NOT REACHABLE OR SIMILAR PROBLEM PARSING")
      return 1
      #pixelit.skipApp()
      #quit()
    try:
      nextDate = getTatortdate(rawhtml)
      nextTitle= getTatorttitle(rawhtml)
      nextSeriesName=getSeriesname(rawhtml)
      return nextSeriesName, nextTitle, nextDate
    except:
      print("[INFO] No Krimi found under",krimiurl)
      return 1
      
def getTatortdate(html):
    for onAir in html:
        tatortdate=onAir.find(class_='dachzeile')
        tatortdate = BeautifulSoup(str(tatortdate),'html.parser')
        tatortdate = tatortdate.text.strip()
        #TODO: on saturdays date might be set to "morgen" instead of date
        #tatortdate = dateConvert(tatortdate)
        #tatortdate = tatortdate.strftime("%a. %d.%m. %H:%M Uhr")
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
      return "Polizeiruf 110"
    elif seriesName.find("Tatort") !=-1:
      #print("Tatort")
      return "Tatort"
    else:
      print("[ERROR] KEIN SERIENNAME GEFUNDEN!")
      return "KEIN SERIENNAME GEFUNDEN"   

class Krimi:
  def __init__(self,myseries,mytitle,mytime):
    self.series = myseries
    self.title = mytitle
    self.time = mytime

  def getSeries(self):
    return self.series
    
  def getTitle(self):
    return self.title
    
  def getTime(self): 
    return self.time


def compare(krimiurls):
  krimiliste=[]
  # for all Series get the next event and save as Object
  for url in krimiurls:    
    if checktatort(url) != 1:
      mySeries,myTitle,myTime = checktatort(url)
      krimi_tmp=Krimi(mySeries,myTitle,myTime)
      #print("[DEBUG] found krimi event", krimi_tmp.getTime(),krimi_tmp.getTitle(), krimi_tmp.getSeries())
      krimiliste.append(krimi_tmp)

  krimitime=[]
  # Check for primetime
  # print("[DEBUG] check for primetime")
  for krimi in krimiliste:
    #print("Krimiliste is before")
    #for krimi2 in krimiliste:
    #    print(krimi2.getTitle())  
    separator = "|"
    out = krimi.getTime().split(separator,1)[1]
    out = datetime.datetime.strptime(out," %H:%M Uhr")
    present = datetime.datetime.today()
    if out.hour!=20 or out < present:
      #print("is not primetime or in the past")
      krimiliste.remove(krimi)
    #print("Krimiliste is after")
    #for krimi2 in krimiliste:
    #    print(krimi2.getTitle())

  #check for empty list:
  if not krimiliste:
    print("[INFO] No krimi found / left")
    msg="Kein Tatort/Polizeiruf in naher Zukunft!"
    myicon="[693,693,65535,693,693,693,693,693,65535,63488,65535,65535,65535,693,693,63488,693,693,63488,693,693,65535,63488,693,693,65535,65535,63488,693,63488,65535,693,65535,693,65535,693,63488,693,693,65535,693,693,65535,63488,693,63488,693,65535,65535,65535,63488,65535,65535,65535,63488,65535,693,63488,65535,693,693,65535,693,63488]"
    pixelit.sendApp(text_msg=msg,
      red=255,
      green=255,
      blue=255,
      icon=myicon,
      bigFont="false",
      scrollText="auto",
      centerText="false",
      )
    return(msg,False)
    #quit()
    
  
  # Compare dates / convert "heute" to date to find the next Krimi
  for krimi in krimiliste:
    print("[INFO] Found Krimi:",krimi.getSeries(),krimi.getTitle(),krimi.getTime())
    separator = "|"
    out=krimi.getTime().rsplit(separator,1)[0]
    if "Heute" in out:
      #print("string heute gefunden")
      out = datetime.datetime.today().strftime('%d.%m.')
      out = datetime.datetime.strptime(out,"%d.%m.").date()
      print(out, type(out))
    elif "Morgen" in out:
      #print("string morgen gefunden")
      out = datetime.datetime.today() + datetime.timedelta(days=1)
      out = out.strftime('%d.%m.')
      out = datetime.datetime.strptime(out,"%d.%m.").date() 
    else:
      out = out[5:]
      out = datetime.datetime.strptime(out,"%d.%m. ").date()
    krimitime.append(out)

  index=krimitime.index(min(krimitime)) #find smallest date and get index of list
  nextkrimi=krimiliste[index]

  #check for old year
  #print("[DEBUG]", nextkrimi.getTime())

  msg ="Nächster "+ nextkrimi.getSeries() + ": »" + nextkrimi.getTitle() + "«, " + str(nextkrimi.getTime())
  krimi2ledmatrix(msg,True)
  return(msg,True)


if __name__ == "__main__":
    myappname="tatortARD"

    tatorturl="https://www.daserste.de/unterhaltung/krimi/tatort/vorschau/index.html"
    polizeirufurl="https://www.daserste.de/unterhaltung/krimi/polizeiruf-110/vorschau/index.html"
    krimiurls=[tatorturl,polizeirufurl]

    krimiliste=[]

    # fresh data
    if pixelit.exceedsTimeLimit(myappname,config.tatort['fetchEveryMinutes']):
        pixelit.writeDataToFile(compare(krimiurls),myappname) #compare, send, and save
    else:
      try:
        data=pixelit.readDataFromFile(myappname) #read old data from cache
        krimi2ledmatrix(data)
      except:
        pixelit.writeDataToFile(compare(krimiurls),myappname) #compare, send, and save

    
