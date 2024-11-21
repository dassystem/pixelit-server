#!/usr/bin/python3
# -*- coding: utf-8 -*-

import config

import os
import subprocess
import time
from datetime import datetime
import pathlib
import pixelit



class AppLoop:
  def __init__(self):
    self.applist=[]

  def loadApps(self):
    for appname,apppath in config.apps.items():
      # make relative path to absolute paths
      # print("relative path",apppath)
      apppath = os.path.abspath(apppath)
      # print("absolute path",apppath)
      tmpapp=App(appname, apppath)
      self.add(tmpapp)

  def getApplist(self):
    return self.applist

  def printApps(self):
    print("[INFO] SERVER found",len(self.applist),"apps:")
    for index, app in enumerate(self.applist, start=1):
      print("[INFO] SERVER: App #"+str(index), app.getAppname(),": in",app.getPath())

  def add(self, newApp):
    self.applist.append(newApp)

  def loopApps(self):
    while True:
      for i in self.getApplist():
        try:
          checkTime()
          subprocess.call(i.getPath()) #calling individual .py scripts
          print("\n[DEBUG] Advancing to next app \n")
        except subprocess.CalledProcessError as err:
         print("[ERROR] Something happend calling an app in the app loop.")
        except PermissionError:
         print("[ERROR] No permission for",str(i.getPath()),"Is this a correctly encoded python script?")
  


class App:
  def __init__(self,appname,path):
      self.appname=appname
      self.path=path

  def getAppname(self):
    return (self.appname)
    
  def getPath(self):
    return (self.path)


def checkTime():
  try:
    current_time = datetime.now().time()
    start = datetime.strptime(config.setup['starttime'], '%H:%M').time()
    stop = datetime.strptime(config.setup['stoptime'], '%H:%M').time()
    print("[DEBUG] It is", current_time, "we start at", start,"and we stop at",stop)
    if (current_time > start) and (current_time < stop):
      pixelit.pixelItSleep(False)
    else:
      pixelit.pixelItSleep(True)
  except:
    print("[INFO] No start and stop time found in config.py")
    pass
    
def text(mytext):
  print("\n===========================")
  print(mytext)
  print("===========================\n")


if __name__ == "__main__":

  text("WELCOME TO PIXELIT SERVER")

  appLoop=AppLoop()
  appLoop.loadApps()
  print("[INFO] SERVER found these apps:")
  appLoop.printApps()

  text("SERVER Apploop starts now!")

  appLoop.loopApps()
  
