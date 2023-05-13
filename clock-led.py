#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pixelit
import config

from datetime import datetime


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
