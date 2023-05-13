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

class KrimiEvent:
    """Ein Ereigniss mit Tatort oder Polizeiruf"""

    def __init__(self, series, date, airtime, title, year, number, rebroadcast):
        self.date = datetime.datetime.strptime(date.lstrip(), '%d.%m.')
        self.airtime = airtime
        self.title = title
        self.series = series
        self.number = number
        self.year = year
        self.rebroadcast = rebroadcast

    def getKrimiData(self):
        return "" + self.series + " " + \
            self.date.strftime('%d.%m.') + " " + \
            self.airtime + " " + self.title

    def getDate(self):
        return self.date

    def getNumber(self):
        return self.number

    def getYear(self):
        return self.year

    def getRebroadcast(self):
        return self.rebroadcast

    def printKrimiData(self):
        print(
            self.series,
            self.date.strftime('%d.%m.'),
            self.airtime,
            self.title,
            "WHD?:",self.rebroadcast)

def next_weekday(weekday):
    today = date.today()
    days_ahead = weekday - today.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return today + datetime.timedelta(days_ahead)


def scrapHTML(myurl):
    rawdata = requests.get(myurl)
    html = rawdata.content
    soup = BeautifulSoup(html, 'html.parser')
    # get sendetermine-2019-wochentag
    return soup.find_all(
        True, {'class': ['sendetermine-2019-even', 'sendetermine-2019-odd']})

def getDetailUrl(number, myurl):
    """ get the detailpage for more information like first aired year
    /tatort/folgen/1095-anne-und-der-tod-1287944
    """
    rawdata = requests.get(myurl)
    html = rawdata.content
    plainHTML = BeautifulSoup(html, 'html.parser')

  # find DetailURL
    for link in plainHTML.find_all('a'):
        if link.get('href').find(number) != -1:
            suburl = link.get('href')
            fullurl = "https://www.fernsehserien.de"+suburl
            logging.debug("Found", fullurl)
            return (fullurl)


def getfirstAired(detailUrl):
    rawdata = requests.get(detailUrl)
    html = rawdata.content
    plainHTML = BeautifulSoup(html, 'html.parser')

    firstAiredDate = plainHTML.find_all('ea-angabe-datum') #<ea-angabe-datum>
    firstAiredDate = BeautifulSoup(
        str(firstAiredDate[0]), 'html.parser').text[3:]  # "19.05.2019"
    firstAiredDate = datetime.datetime.strptime(firstAiredDate, '%d.%m.%Y') #convert to date
    logging.debug("First aired",firstAiredDate)
    return firstAiredDate


def checkForRebroadcast(krimiFirstAired):
    """ Check if the show first aired last year or before"""
    if krimiFirstAired.year < date.today().year:
#        print("[DEBUG] First aired year ", krimiFirstAired.year,              "is older than today", date.today().year)
        return True
    else:
#        print("[DEBUG] First aired year ", krimiFirstAired.year,              "is from this year", date.today().year)
        return False


def sortByDate(data):
    return data['date']


def findEvents(myurl, series, sendungs_liste):
    next_sunday = next_weekday(6)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
    format = "%d.%m."
    shortdate = (next_sunday.strftime(format))

    output = scrapHTML(myurl)
    for onAir in output:
        if ">So<" in str(onAir):  # check for sundays only
            #print("DEBUG",myurl, str(onAir))
            if shortdate in str(onAir):  # check if it is the NEXT sunday
                sendezeit = onAir.find(
                    class_='sendetermine-2019-uhrzeit-smartphone')
                krimi_sendezeit = sendezeit.contents[0].get_text().replace(
                    '–', '-')
                krimi_title = onAir.find(
                    class_='sendetermine-2019-episodentitel')
                krimi_title = '»' + krimi_title.contents[0].rstrip() + '«'
                krimi_date = onAir.find(class_='only-smartphone2')
                krimi_date = krimi_date.contents[0]
                krimi_number = onAir.find(
                    class_='sendetermine-2019-staffel-und-episode').contents[0]
                # print("number",krimi_number)
                krimi_serie = series

                # Check for Rebroadcast:
                krimi_year = getfirstAired(getDetailUrl(krimi_number, myurl))
                krimi_rebroadcast = checkForRebroadcast(krimi_year)

                next_krimi = KrimiEvent(
                    krimi_serie, krimi_date, krimi_sendezeit, krimi_title, krimi_year, krimi_number, krimi_rebroadcast)
#                next_krimi.printKrimiData()
                sendungs_liste.append(next_krimi)

    return sendungs_liste

def checkKrimi():
# returns  true / false for Krimievent on next Sunday
    sendungs_liste = []

    polizeiruf_url = "https://www.fernsehserien.de/polizeiruf-110/sendetermine/das-erste"
    tatort_url     = "https://www.fernsehserien.de/tatort/sendetermine/das-erste"

    sendungs_liste = findEvents(tatort_url, "Tatort", sendungs_liste)
    sendungs_liste = findEvents(
        polizeiruf_url,
        "Polizeiruf 110",
        sendungs_liste)

    sendungs_liste.sort(key=operator.attrgetter('date'))  # (key=sortByDate)

    if (len(sendungs_liste) > 0):
        nextSundayKrimi = True
        mytext = "Nächsten So.: " + sendungs_liste[0].getKrimiData()
        if sendungs_liste[0].getRebroadcast():
            mytext = mytext + " (Wdh.)"
        #print([DEBUG] mytext)
        #ledmatrix.sendledmatrixApp("tatort", mytext,255,255,255,"yesard","false",1,0,1,9)
    else:
        nextSundayKrimi = False
        mytext = "Nächsten Sonntag läuft kein Tatort/Polizeiruf!"
        #print([DEBUG] mytext)
        #ledmatrix.sendledmatrixApp("tatort", mytext,255,255,255,"noard","false",1,0,1,9)

    return nextSundayKrimi, mytext


def krimi2ledmatrix(nextSundayKrimi, msg):
    print("[INFO] Sending to ledmatrix:", msg)
    if nextSundayKrimi:
        myicon="[693,693,65535,693,693,693,693,693,65535,65535,65535,65535,65535,693,693,693,693,693,65535,693,693,65535,693,693,693,65535,65535,65535,693,693,65535,693,65535,693,65535,693,65535,693,693,65535,693,693,65535,693,693,65535,693,65535,65535,65535,693,65535,65535,65535,65535,65535,693,693,65535,693,693,65535,693,65535]"
    else: #no tatort - sad icon
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

if __name__ == "__main__":
    myappname="tatort"
    if pixelit.exceedsTimeLimit(myappname,config.tatort['fechtEveryMinutes']):
        nextSundayKrimi, msg = checkKrimi()   #get all data
        krimi2ledmatrix(nextSundayKrimi, msg)    #send data to ledmatrix
    else:
      try:
        data=pixelit.readDataFromFile(myappname)
      except:
        nextSundayKrimi, msg = checkKrimi()   #get all data
        krimi2ledmatrix(nextSundayKrimi, msg)    #send data to ledmatrix

def testing():
    print("testing")
    for nummer in sendungs_liste:
        print(nummer.getKrimiData())
