#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import random
import pixelit

import feedparser

import config

import datetime
import pytz


class newsItem:
  """A News Message """
  def __init__(self, title, source, link, pubdate, icon):
    self.title = title
    self.source = source
    self.link = link
    self.pubdate = pubdate
    self.icon = icon

  def getTitle(self):
    return self.title

  def getSource(self):
    return self.source

  def getLink(self):
    return self.link

  def getPubdate(self):
    return self.pubdate

  def getIcon(self):
    return self.icon

  def printInfo(self):
    print(self.title,self.source,self.link, self.pubdate)

  

class newsFeed:
  """A RSS Feed URL with icon """

  def __init__(self, url, source, icon):
    self.url = url
    self.source = source
    self.icon = icon

  def getUrl(self):
    return self.url

  def getSource(self):
    return self.source

  def getIcon(self):
    return self.icon

#TODO Newsitem as input, not string
def sendTo(myNews):

  #outputstring="("+myNews.getSource()+") " + myNews.getTitle()
  outputstring=myNews.getTitle()
  

  outputstring=outputstring.replace('"','\"') #escape doublequotes
  outputstring=outputstring.replace("'","\'") #escape singlequotes
  outputstring=outputstring + " +++ "
# name, text_msg,r=255,g=255,b=255,icon=111,force="true",count=1,duration=0,repeat=1,ID=99)
  pixelit.sendApp(
     text_msg=outputstring + "  " + outputstring, #show the message twice
     red=255,
     blue=255,
     green=255,
     icon=myNews.getIcon(),
     bigFont="false",
     scrollText="auto",
     centerText="false",
     )

def url2news(newsFeed): #old getNews()
  """Transform a URL to a News Object and return it"""
  myUrl=newsFeed.getUrl()

  myFeeds = feedparser.parse(myUrl)
  
  newsitems=[]
  itemcount = 0
  maxNewsPerFeed = config.rssnews['itemsPerFeed'] #count of items per feed to grab
  for item in myFeeds.entries:
    if itemcount < maxNewsPerFeed:
      newNewsitem = newsItem(item.title,newsFeed.getSource(),item.link,item.published, newsFeed.getIcon())
      newsitems.append(newNewsitem)
    itemcount= itemcount + 1
  return newsitems

# Print news title, url and publish date
def testNews(news_list):
  print("\n","-"*60)
  print("[TESTING]")
  print("-"*60,"\n")

  for news in news_list:
    print(news.title.text)
    print(news.link.text)
    print(news.pubDate.text)
    print("-"*60)



if __name__ == "__main__":
  news_list=[]

  for feedname,data in config.rssnews['newsfeed'].items():
    try:
      name=str(feedname)
      url=str(data['url'])
      icon=str(data['icon'])
      #print(name,url,icon)
      tmpfeed=newsFeed(url,name,icon)
      news_list.append(tmpfeed)
    except:
      print("[DEBUG] Something wrent wrong importing feeds")

  timezone = pytz.timezone('UTC')
  now = timezone.localize(datetime.datetime.now())
  myappname="rssnews"

  if pixelit.exceedsTimeLimit(myappname,config.rssnews['fechtEveryMinutes']):
    # Load News from the Internets and write to file
    print("[DEBUG] Loading news from the Internets")
    single_newslist=[]
    for feedUrl in news_list: #feed is URL
      newsitems = url2news(feedUrl)
      for item in newsitems:
        single_newslist.append(item)
    # Testing
   # for item in single_newslist:
   #   print("[DEBUG]",item.getSource(),item.getTitle())
    print("[DEBUG] Total amount of news entries:",len(single_newslist))
    print("[Debug] writing new data to cache")
    pixelit.writeDataToFile(single_newslist,myappname)
    full_newslist=single_newslist
  else:
    print("[DEBUG] Loading news from cache")
    full_newslist=pixelit.readDataFromFile(myappname)
    #for item in full_newslist:
    #  print("[DEBUG]",item.getSource(),item.getTitle())

  
  # get random news and send to pixelit      
  randomNews=random.choice(full_newslist)
  print("[INFO] Sending ("+randomNews.getSource()+") »",randomNews.getTitle(),"« to LED-Matrix")
  sendTo(randomNews)
