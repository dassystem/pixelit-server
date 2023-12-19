#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import datetime
from datetime import date
from bs4 import BeautifulSoup
import operator

import pixelit
import config
import asyncio

import logging

def scrapHTML(myurl):
    rawdata = requests.get(myurl)
    html = rawdata.content
    soup = BeautifulSoup(html, 'html.parser')
    # get sendetermine-2019-wochentag
    return soup.find_all(
        True, {'class': ['contentStageCon']})

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
    tatorturl="https://www.daserste.de/unterhaltung/krimi/tatort/vorschau/index.html"
    nextDate = getTatortdate(tatorturl)
    print("Date:", nextDate)
    nextTitle= getTatorttitle(tatorturl)
    print("Title:", nextTitle)

    return nextTitle, nextDate

def getTatortdate(url):
    output = scrapHTML(url)
    for onAir in output:
        tatortdate=onAir.find(class_='dachzeile')
        #print(tatortdate)
        tatortdate = BeautifulSoup(str(tatortdate),'html.parser')
        tatortdate = tatortdate.text.strip()
        #tatortdate=BeautifulSoup.font.contents(tatortdate, 'html.parse').text
    return tatortdate
    
def getTatorttitle(url):
    output = scrapHTML(url)
    for onAir in output:
        tatorttitle=onAir.find(class_='headline')
        #print(tatortdate)
        tatorttitle = BeautifulSoup(str(tatorttitle),'html.parser')
        tatorttitle = tatorttitle.text.strip()
        #tatortdate=BeautifulSoup.font.contents(tatortdate, 'html.parse').text
    return tatorttitle   


if __name__ == "__main__":
    myappname="tatort"
    myTitle,myTime = checktatort()

    msg ="Nächster Krimi: »" + str(myTitle) + "« am " + str(myTime)
    krimi2ledmatrix(msg)