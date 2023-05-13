#!/usr/bin/python3
# -*- coding: utf-8 -*-

import config

import os
import subprocess
import time
import pathlib
import pixelit

class AppLoop:
  def __init__(self):
    self.applist=[]

  def loadApps(self):
    currentpath=pathlib.Path(__file__).parent.resolve()
    #print("[DEBUG]",str(currentpath))
    for file in os.listdir(str(currentpath)+"/active-apps"):
      if not file.endswith("config.py"):
        if not file.endswith("pixelit.py"):
          if file.endswith(".py"):
            #print(file)
            tmp=App(file,str(currentpath)+"/active-apps/"+file)
            self.add(tmp)

  def getApplist(self):
    return self.applist

  def printApps(self):
    print("[INFO] SERVER found",len(self.applist),"apps:")
    for i in self.applist:
      print("[INFO] SERVER", i.getAppname(),": in",i.getPath())

  def add(self, newApp):
    self.applist.append(newApp)

class App:
  def __init__(self,appname,path):
      self.appname=appname
      self.path=path

  def getAppname(self):
    return (self.appname)
    
  def getPath(self):
    return (self.path)
    
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
  
  while True:
    for i in appLoop.getApplist():
      subprocess.call(i.getPath()) #calling individual .py scripts

