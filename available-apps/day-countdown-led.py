#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import *

# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config


# TODO: How to configure multiple dates?


def getTargetDate():
  try:
    return datetime.strptime(config.daycountdown['targetdate'],'%Y-%m-%d').date()  
  except: #What if no target date is configured?
    print("[DEBUG]",myappname,": Found no working config")
    pixelit.skipApp()
    quit()
    return -1
    
def showDays():
  now = date.today()
  daycount=str(getTargetDate()-now).split(',')[0] 

  ####### Icons:
  # Calendar:
  calendar="[0,65535,0,0,0,65535,0,0,65535,65535,65535,65535,65535,65535,65535,0,65535,0,0,0,0,0,65535,0,65535,0,48599,0,48599,0,65535,0,65535,0,0,0,0,0,65535,0,65535,0,65535,0,48599,0,65535,0,65535,0,0,0,0,0,65503,0,65535,65535,65535,65535,65535,65535,65535,0]"
  #
  holiday="[65351,65351,31801,31801,36361,36361,36361,36361,65351,65351,31801,31801,31801,36361,14628,36361,31801,31801,31801,31801,31801,14628,31801,36361,31801,31801,31801,31801,31801,14628,31801,36361,31801,31801,31801,31801,31801,14628,31801,31801,31801,31801,31801,65024,65024,65024,31801,31801,31801,65024,65024,65024,65024,65024,65024,31801,2612,2612,2612,2612,2612,2612,2612,2612]"
  #
  birthday="[0,64164,0,0,64164,0,64164,0,0,61309,0,0,61309,0,61309,0,0,61309,0,0,61309,0,61309,0,62226,62226,62226,62226,62226,62226,62226,62226,0,65535,64986,65535,65535,65535,64986,0,0,64986,65535,64986,65535,64986,65535,0,0,65535,65535,65535,64986,65535,65535,0,62226,62226,62226,62226,62226,62226,62226,62226]"
  #
  xmas="[0,0,0,0,65514,0,0,0,0,0,0,672,7267,7267,0,0,0,0,0,672,7267,53573,0,0,0,0,672,672,7267,7267,7267,0,0,0,53573,672,53573,7267,7267,0,0,672,672,672,7267,7267,53573,7267,0,672,672,53573,672,672,672,672,0,0,0,0,672,0,0,0]"

  try:
    match config.daycountdown['topic']:
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
    print("[INFO] Sending to LED Matrix:",daycount,"until",config.daycountdown['targetname'])
    pixelit.sendApp(
      text_msg=daycount+" days until "+config.daycountdown['targetname'],
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
  showDays()

