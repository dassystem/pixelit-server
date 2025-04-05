#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import *

# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config
import random

# TODO: Configure multiple dates. Show them randomly or in sequence?
# TODO: For recurring dates leaveout the year?


####### Icons:
# Calendar:
calendar="[0,65535,0,0,0,65535,0,0,65535,65535,65535,65535,65535,65535,65535,0,65535,0,0,0,0,0,65535,0,65535,0,48599,0,48599,0,65535,0,65535,0,0,0,0,0,65535,0,65535,0,65535,0,48599,0,65535,0,65535,0,0,0,0,0,65503,0,65535,65535,65535,65535,65535,65535,65535,0]"
#
holiday="[65351,65351,31801,31801,36361,36361,36361,36361,65351,65351,31801,31801,31801,36361,14628,36361,31801,31801,31801,31801,31801,14628,31801,36361,31801,31801,31801,31801,31801,14628,31801,36361,31801,31801,31801,31801,31801,14628,31801,31801,31801,31801,31801,65024,65024,65024,31801,31801,31801,65024,65024,65024,65024,65024,65024,31801,2612,2612,2612,2612,2612,2612,2612,2612]"
#
birthday="[0,64164,0,0,64164,0,64164,0,0,61309,0,0,61309,0,61309,0,0,61309,0,0,61309,0,61309,0,62226,62226,62226,62226,62226,62226,62226,62226,0,65535,64986,65535,65535,65535,64986,0,0,64986,65535,64986,65535,64986,65535,0,0,65535,65535,65535,64986,65535,65535,0,62226,62226,62226,62226,62226,62226,62226,62226]"
#
xmas="[0,0,0,0,65514,0,0,0,0,0,0,672,7267,7267,0,0,0,0,0,672,7267,53573,0,0,0,0,672,672,7267,7267,7267,0,0,0,53573,672,53573,7267,7267,0,0,672,672,672,7267,7267,53573,7267,0,672,672,53573,672,672,672,672,0,0,0,0,672,0,0,0]"



class targetDate():
    """ A date item with date, describtion and icon"""
    def __init__(self,date,name,topic):
        self.date = date
        self.name = name
        self.topic = topic

    def getDate(self):
        return self.date

    def getName(self):
        return self.name

    def getTopic(self):
        return self.topic

    def printInfo(self):
        print("[DEBUG]",self.date,self.name,self.topic)

        

def getTargetList():
    date_list=[]
    for entry,data in config.daycountdown['entry'].items():
      #print("entry:",entry, "data", data)
      if (data.get('topic') is None): #check for missing icon
        newEntry=targetDate(str(data['targetdate']),str(data['targetname']),'calendar')
      else:   
        newEntry=targetDate(str(data['targetdate']),str(data['targetname']),str(data['topic']))
      newEntry.printInfo()
      date_list.append(newEntry)

    return random.choice(date_list)       # return one value by random
      



def getTargetDate(myEntry):
  #myEntry.printInfo()
  try:
    return datetime.strptime(myEntry.getDate(),'%Y-%m-%d').date()  
  except: #What if no target date is configured?
    print("[DEBUG]",myappname,": Found no working config")
    pixelit.skipApp()
    quit()
    return -1
    
def showDays(myEntry):
  now = date.today()
  daycount=str(getTargetDate(myEntry)-now).split(',')[0] 

  try:
    match myEntry.getTopic():
      case 'birthday':
        myicon=birthday
      case 'holiday':
        myicon=holiday
      case 'xmas':
        myicon=xmas
      case 'calendar':
        myicon=calendar
  except: 
    myicon=calendar
    print("[DEBUG]",myappname,"using fallback icon")
    
  if int(daycount.split(' ')[0]) >= 0: #date is in the future
    print("[INFO] Sending to LED Matrix:",daycount,"until",myEntry.getName())
    pixelit.sendApp(
      text_msg=daycount+" days until "+myEntry.getName(),
      red=255,
      green=255,
      blue=255,  
      bigFont="false",
      scrollText="auto",
      centerText="true",
      icon=myicon,
      )  
  else: #date is in the past
    print("[DEBUG]",myappname,"target date is in the past")
    pixelit.skipApp()

if __name__ == "__main__":
  myappname="day-countdown"
  showDays(getTargetList())

