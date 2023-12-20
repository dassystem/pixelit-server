#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime

# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config


def showTime():
  now = datetime.now()
  current_time = now.strftime("%H:%M")

  print("[INFO] Sending to LED Matrix:",current_time)
  pixelit.sendText(
    text_msg=current_time,
    red=255,
    green=255,
    blue=255,  
    bigFont="false",
    scrollText="auto",
    centerText="true"
    )  

if __name__ == "__main__":
  showTime()
