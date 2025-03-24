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
      icon="[0,65535,0,0,0,65535,0,0,65535,65535,65535,65535,65535,65535,65535,0,65535,0,0,0,0,0,65535,0,65535,0,48599,0,48599,0,65535,0,65535,0,0,0,0,0,65535,0,65535,0,65535,0,48599,0,65535,0,65535,0,0,0,0,0,65503,0,65535,65535,65535,65535,65535,65535,65535,0]"
      )  
  else: #date is in the past
    print("[DEBUG]",myappname,"target date is in the past")
    pixelit.skipApp()

if __name__ == "__main__":
  myappname="day-countdown"
  showDays()

