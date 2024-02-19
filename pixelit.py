#
# This is a helper library for sending information to pixelit LED matrix
#
# See https://pixelit-project.github.io/
#     https://github.com/pixelit-project
#
# For old awtrix see:
# See https://awtrixdocs.blueforcer.de/#/en-en/README?id=awtrix
#     https://awtrixdocs.blueforcer.de/#/de-de/api
# 

import requests
import config
import paho.mqtt.client as mqtt
import pickle
import time

import os
import datetime
import pytz

import threading



""" Helping apps saving data to local cache file """
def writeDataToFile(data,appname):
  filename="."+appname+"-data.cache"
  file=open(filename,"wb")
  pickle.dump(data,file)
  file.close()

def readDataFromFile(appname):
  filename="."+appname+"-data.cache"
  print("[pixelit.py] reading",filename)
  file=open(filename,"rb")
  out=pickle.load(file)
  file.close()
  return out

""" Helping apps with scheduling timed requests and caching """
def writeTimestampToFile(time,appname):
  timestamp="."+appname+"-timestamp.cache"
  file=open(timestamp,"wb")
  pickle.dump(time,file)
  file.close()

def readTimestampFromFile(appname):
  timestamp="."+appname+"-timestamp.cache"
  print("[pixelit.py] reading",timestamp)
  file=open(timestamp,"rb")
  out=pickle.load(file)
  file.close()
  return out



"""Check with timestamps, if a set time limit is exceeded. """
def exceedsTimeLimit(appname,timeLimitMinutes):
  timezone = pytz.timezone('UTC')
  now = timezone.localize(datetime.datetime.now())
  try:
    oldtime = readTimestampFromFile(appname)
  except:
    print("[INFO] no timestamp there. creating one.")
    writeTimestampToFile(now,appname)
    #oldtime = readTimestampFromFile(appname)
    return True
  
  timediff=now-oldtime
  #print("[DEBUG] Timediff is", timediff,". Checking for timeLimit:",timeLimitMinutes)
  if round(timediff.total_seconds()) <=timeLimitMinutes:
    #print ("[DEBUG] Timediff ("+str(round(timediff.total_seconds()))+") is smaller than limit",timeLimitMinutes)
    return False
  else:
    #print ("[DEBUG] Timediff is larger than limit")
    writeTimestampToFile(now,appname)
    return True


# pixelItSleep(True)  = Display off
# pixelItSleep(False) = Display on
""" Turns display on and off"""
def pixelItSleep(bool=True):
  print("[DEBUG]")
  if bool:
    senddata='{"sleepMode": true}'
  else: 
    senddata='{"sleepMode": false}'
  print("[DEBUG] Display is in sleepmode",bool)
  sending(senddata) 


""" Helper to convert RGB values """
def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


# Read from config.py
scrollTextDelay = str(config.setup['scrollTextDelay'])


"""Getting the shown charaters for a display time approximation """
def calculateDisplayDuration(msgTextLen):
  minTimePerApp=config.setup['minSecondsPerApp']
  chars=msgTextLen
  if chars == -1:
    print("[DEBUG] Time calc: Reading -1 Characters. Skipping app")
    # No sleep, try next app
  else:
    textduration=round((chars + 8) * 4.7 * config.setup['scrollTextDelay']/1000,2)
    if (textduration < minTimePerApp):
      # Display text is very short. Wait a minimal amount of time.
      print("[DEBUG] Time calc: Characters:",str(chars)+". Waiting for",minTimePerApp,"seconds")
      time.sleep(minTimePerApp)
    else:
      # Display text is long enough. Calculate correct length and wait
      print("[DEBUG] Time calc: Characters:",str(chars)+". Waiting for",textduration,"seconds")
      time.sleep(textduration)


def skipApp():
  calculateDisplayDuration(-1)

# dirty: just send an App instead
def sendNotification(text_msg,red=255,green=255,blue=255,icon=111,bigFont="false",scrollText='auto',centerText="false"):
  sendApp(text_msg,red,green,blue,icon,bigFont,scrollText,centerText)

"""sending text without bitmap """
def sendText(text_msg="Hello World",red=255,green=255,blue=255,bigFont="false",scrollText='auto',centerText="true"):
  senddata = '{ \
        "text": { \
          "textString": " '+text_msg+'",\
          "bigFont": '+bigFont+',\
          "scrollText": "'+scrollText+'",\
          "scrollTextDelay": '+scrollTextDelay+',\
          "centerText": '+centerText+',\
          "position": {\
            "x" : 1,\
            "y" : 1\
          },\
          "color": {\
            "r": "'+str(red)+'",\
            "g": "'+str(green)+'",\
            "b": "'+str(blue)+'"\
          },\
          "hexColor": "'+rgb_to_hex(red,green,blue)+'"\
        }\
      }'
  sending(senddata)
  calculateDisplayDuration(len(text_msg))



def sendApp(text_msg="Hello World",red=255,green=255,blue=255,icon="[255]",bigFont="false",scrollText='auto',centerText="true"):
  senddata = '{ \
        "bitmap": {\
          "data": '+icon+',\
          "position": {\
            "x": 0,\
            "y": 0\
          },\
          "size": {\
            "width": 8,\
            "height": 8\
          }\
        },\
        "text": { \
          "textString": " '+text_msg+'",\
          "bigFont": '+bigFont+',\
          "scrollText": "'+scrollText+'",\
          "scrollTextDelay": '+scrollTextDelay+',\
          "centerText": '+centerText+',\
          "position": {\
            "x" : 1,\
            "y" : 1\
          },\
          "color": {\
            "r": "'+str(red)+'",\
            "g": "'+str(green)+'",\
            "b": "'+str(blue)+'"\
          },\
          "hexColor": "'+rgb_to_hex(red,green,blue)+'"\
        }\
      }'
  #print("[SERVER][DEBUG]",senddata)
  sending(senddata)  
  calculateDisplayDuration(len(text_msg))


# dirty: just send an App instead
def sendTmpApp(appname, text_msg,red=255,green=255,blue=255,icon=111,lifetime=1):
  sendApp(appname,text_msg,red,green,blue,icon,False,1,1,1,id=99)

""" helper function to send data via REST or MQTT to the led matrix"""
def sending(senddata):
  if config.mqtt['usage']==True:
    broker=str(config.mqtt['broker'])
    port=config.mqtt['port']
    topic=str(config.mqtt['topic'])+'/setScreen'
    QOS = config.mqtt['qos']
    client1= mqtt.Client("control1")                           
    client1.connect(broker,port)  
    #print("[DEBUG] Sending to",topic,"@",broker)
    client1.publish(topic,senddata,qos=QOS)
    client1.loop()
  else: ## Send via REST
    for pixelitUrl in config.setup['pixeliturls']:
      # create threads for multiple displays
      sendthread = threading.Thread(target=sendToOneDisplay, args=(pixelitUrl, senddata))
      sendthread.start()

def sendToOneDisplay(pixelitUrl,senddata):
  try:
    sendurl = pixelitUrl + '/api/screen'
    sendheaders = {'Content-Type': 'application/json'}
    requests.post(url=sendurl, data=senddata.encode('utf-8'), headers=sendheaders)
  except: 
    print("[ERROR] Could not reach PixelIt at",pixelitUrl)  