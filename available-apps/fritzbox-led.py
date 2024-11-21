#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config
import time
import re

from fritzconnection.lib.fritzstatus import FritzStatus


arrowUp="[0,0,0,63169,63169,0,0,0,0,0,63169,63169,63169,63169,0,0,0,63169,63169,63169,63169,63169,63169,0,63169,63169,63169,63169,63169,63169,63169,63169,0,0,0,63169,63169,0,0,0,0,0,0,63169,63169,0,0,0,0,0,0,63169,63169,0,0,0,0,0,0,63169,63169,0,0,0]"

arrowDown="[0,0,0,63169,63169,0,0,0,0,0,0,63169,63169,0,0,0,0,0,0,63169,63169,0,0,0,0,0,0,63169,63169,0,0,0,63169,63169,63169,63169,63169,63169,63169,63169,0,63169,63169,63169,63169,63169,63169,0,0,0,63169,63169,63169,63169,0,0,0,0,0,63169,63169,0,0,0]"

def send2matrix(printtext,printicon): 
  print("[INFO] Sending to LED Matrix:",printtext)
  pixelit.sendApp(
    text_msg=printtext,
    red=255,
    green=255,
    blue=255,
    icon=printicon,
    bigFont="false",
    scrollText="auto", 
    centerText="true",
    noWait=False
    )
  time.sleep(5)


def checkBitrates():
  fc = FritzStatus(address=config.fritzbox['ip'],  user=config.fritzbox['user'], password=config.fritzbox['password'])

  bitrates=fc.str_max_bit_rate # ('22.7 MBit/s', '44.0 MBit/s')
  print(bitrates)
  bitrates=re.findall("'([^']*)'", str(bitrates))
  print(bitrates)
  downspeed=bitrates[1]
  #downspeed=downspeed[:-6]
  upspeed=bitrates[0]
  #upspeed=upspeed[:-6]
  print("Down/Up",downspeed,upspeed)

  send2matrix(downspeed,arrowDown)
  send2matrix(upspeed,arrowUp)
  return downspeed, upspeed
    

if __name__ == "__main__":
  myappname="fritzbox"
  
  #caching
  if pixelit.exceedsTimeLimit(myappname,config.fritzbox['fetchEveryMinutes']):
    data=checkBitrates()
    pixelit.writeDataToFile(data,myappname)
  else:
    try:
      data=pixelit.readDataFromFile(myappname)
      downspeed=data[0]
      upspeed=data[1]
      send2matrix(downspeed,arrowDown)
      send2matrix(upspeed,arrowUp)
    except:
      data=checkBitrates()
      pixelit.writeDataToFile(data,myappname)
