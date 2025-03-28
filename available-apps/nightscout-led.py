#!/usr/bin/python3
# -*- coding: utf-8 -*-

# since libre 2 sends data all 5min it is sufficient to set the request every 5 minutes

import requests
import json
import datetime
import pytz

# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config



def test():
  print(glucose,direction,color) #check values
  
#check if the URL exists and is 200 OK
def testUrl(url):
  try:
    request_response = requests.head(url, timeout=3)
    status_code = request_response.status_code
    website_is_up = status_code == 200
    #print(website_is_up)
    if not (website_is_up):
      sendError()
      quit() #hardquit on error
  except:
    print("[ERROR] Issues connecting to nightscout on",url)
    sendError()
    quit()


def sendError():
  print("[ERROR] URL NOT REACHABLE")    
  pixelit.sendApp(text_msg="ERROR: NIGHTSCOUT NOT REACHABLE",
                    red=255,
                    green=0,
                    blue=0,
                    icon="[0,0,0,0,0,0,0,0,0,63488,63488,0,0,63488,63488,0,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,0,63488,63488,63488,63488,63488,63488,0,0,0,63488,63488,63488,63488,0,0,0,0,0,63488,63488,0,0,0]",
                    bigFont="false",
                    scrollText="auto",
                    centerText="true",
                    )

#sendGlucose(glucose, r_color, g_color, b_color, iconnumber)
def sendGlucose(glucose,r_color=255, g_color=255, b_color=255, iconnumber=1037):
  pixelit.sendApp(
     text_msg=str(glucose),
     red=r_color,
     green=g_color,
     blue=b_color,
     icon=iconnumber,
     bigFont="false",
     scrollText="auto",
     centerText="true",
     )
  print("[INFO]","Send",str(glucose),"to LED-matrix")


# check for live data
def checkdatatime(nsEntry):
  lastdata = (nsEntry[0]['dateString'])
  lastdata_obj = datetime.datetime.strptime(lastdata, '%Y-%m-%dT%H:%M:%S.%fZ')
  timezone = pytz.timezone('UTC')
  lastdata_obj = timezone.localize(lastdata_obj)
  timezone = pytz.timezone('Europe/Berlin')
  now = timezone.localize(datetime.datetime.now())
  timediff=abs(now-lastdata_obj)

#  print("[DEBUG] Time:\n now:     ",str(now),"\n last data", lastdata_obj, "\n timediff ", timediff)

# Check if data is older than 30 min
  if round(timediff.seconds/60) <=30:
    print("[OK] - timedifference is", str(round(timediff.seconds/60)), "minutes")
  else:  #end the program, if there is no live data
         # TODO: make this a function
    error_msg= "ERROR: NO DATA RECIEVED FOR "+str(round(timediff.seconds/60))+" min"
    print(error_msg)
    pixelit.sendApp(
      text_msg=error_msg,
      red=255,
      green=0,
      blue=0,
      icon="[0,0,0,0,0,0,0,0,0,63488,63488,0,0,63488,63488,0,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,63488,0,63488,63488,63488,63488,63488,63488,0,0,0,63488,63488,63488,63488,0,0,0,0,0,63488,63488,0,0,0]",
      bigFont="false",
      scrollText="auto",
      centerText="false",
      )
    quit() #hardquit on error



def getEntryUrl():
  return config.nightscout['baseurl'] + "/api/v1/" + "entries" + "/current.json?token=" + config.nightscout['token']

def getProfileUrl():
  return config.nightscout['baseurl'] + "/api/v1/" + "profile" + "/current.json?token=" + config.nightscout['token']


def getProfileData(url):
  try:
  #  print("Getting profiledata?")
  #  print("url", url)
  #  a = requests.get(url)
  #  print("a",a)
  #  b = json.dumps(requests.get(url).json())
  #  print("b",b)
  #  c = json.loads(json.dumps(requests.get(url).json()))
  #  print("c",c)
    return json.loads(json.dumps(requests.get(url).json()))
  except: # json.decoder.JSONDecodeError:
    print("ERROR: loading profile data. Is nightscout available?")

## main program:
if __name__ == "__main__":

####### Profile Stuff
#
# TODO: check for profile errors
  # Build URLs with the token to access entries and the profile settings
  entryurl    = getEntryUrl()
  testUrl(entryurl) # check, if nightscout is available
  profileurl  = getProfileUrl()
  profileData = getProfileData(profileurl)

  # # # # # 
  # Getting Data from nightscout profile
  #

  nsDefaultProfile = profileData['defaultProfile']
  
  glucose_low  = profileData['store'][nsDefaultProfile]['target_low' ][0]['value']
  glucose_high = profileData['store'][nsDefaultProfile]['target_high'][0]['value']
  glucose_veryhigh = glucose_high + 60


  entrydata=json.dumps(requests.get(entryurl).json())
  mydata = json.loads(entrydata)
  checkdatatime(mydata)   # check, if values are too old
  
  try:
    glucose   = (mydata[0]['sgv'])
    direction = (mydata[0]['direction'])
  except: 
    print('[ERROR] - Data unreadable or incorrect format')  
    

  # # # # #
  # calculate the output / color    
  #
  
  color="[255,255,255]" #default text color
  if glucose < glucose_low:
    r_color = 127
    g_color = 50
    b_color = 255
  elif glucose < glucose_high:
    r_color = 0
    g_color = 255
    b_color = 0
  elif glucose < glucose_veryhigh: 
    r_color = 255
    g_color = 255
    b_color = 0
  elif glucose >= glucose_veryhigh: 
    r_color = 255
    g_color = 0
    b_color = 0

  
  # # # # # 
  # Setting the corresponding icon
  #  

  iconnumber="1037" #default heart icon
  # These directions exist
  if direction=="DoubleUp":
    iconnumber="[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2016,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2016,0,0,0,0,0,0,2016,2016,2016,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2016,0,0,0,0,0,0,2016,2016,2016,0,0,0,0,2016,2016,2016,2016,2016,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2016,0,0,0,0,0,0,2016,2016,2016,0,0,0,0,2016,2016,2016,2016,2016,0,0,2016,2016,2016,2016,2016,2016,2016,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2016,0,0,0,0,0,0,2016,2016,2016,0,0,0,0,2016,2016,2016,2016,2016,0,0,2016,2016,2016,2016,2016,2016,2016,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2016,0,0,0,0,0,0,2016,2016,2016,0,0,0,0,2016,2016,2016,2016,2016,0,0,2016,2016,2016,2016,2016,2016,2016,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,2016,0,0,0,0,0,0,2016,2016,2016,0,0,0,0,2016,2016,2016,2016,2016,0,0,2016,2016,2016,2016,2016,2016,2016,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,2016,0,0,0,0,0,0,2016,2016,2016,0,0,0,0,2016,2016,2016,2016,2016,0,0,2016,2016,2016,2016,2016,2016,2016,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,2016,2016,2016,0,0,0,0,2016,2016,2016,2016,2016,0,0,2016,2016,2016,2016,2016,2016,2016,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,2016,2016,2016,2016,2016,0,0,2016,2016,2016,2016,2016,2016,2016,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2016,2016,2016,2016,2016,2016,2016,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]"  
  elif direction=="SingleUp":
    iconnumber="[0,0,0,2016,0,0,0,0,0,0,2016,2016,2016,0,0,0,0,2016,2016,2016,2016,2016,0,0,0,0,2016,2016,2016,0,0,0,0,0,2016,2016,2016,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]"
  elif direction=="FortyFiveUp":
    iconnumber="[0,0,0,0,0,65504,65504,65504,0,0,0,0,0,0,65504,65504,0,0,0,0,0,65504,0,65504,0,0,0,0,65504,0,0,0,0,0,0,65504,0,0,0,0,0,0,65504,0,0,0,0,0,0,65504,0,0,0,0,0,0,65504,0,0,0,0,0,0,0]"    
  elif direction=="Flat":
    iconnumber="[0,0,0,0,0,0,0,0,0,0,0,0,0,2016,0,0,0,0,0,0,0,2016,2016,0,2016,2016,2016,2016,2016,2016,2016,2016,0,0,0,0,0,2016,2016,0,0,0,0,0,0,2016,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]"
  elif direction=="FortyFiveDown":
    iconnumber="[65504,0,0,0,0,0,0,0,0,65504,0,0,0,0,0,0,0,0,65504,0,0,0,0,0,0,0,0,65504,0,0,0,0,0,0,0,0,65504,0,0,0,0,0,0,0,0,65504,0,65504,0,0,0,0,0,0,65504,65504,0,0,0,0,0,65504,65504,65504]"
  elif direction=="SingleDown":
    iconnumber="[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63488,63488,63488,0,0,0,0,0,63488,63488,63488,0,0,0,0,63488,63488,63488,63488,63488,0,0,0,0,63488,63488,63488,0,0,0,0,0,0,63488,0,0,0,0]"
  elif direction=="DoubleDown":
    iconnumber="[0,0,0,0,0,0,0,0,0,0,63488,63488,63488,0,0,0,0,0,63488,63488,63488,0,0,0,0,0,63488,63488,63488,0,0,0,0,63488,63488,63488,63488,63488,0,0,0,0,63488,63488,63488,0,0,0,0,0,0,63488,0,0,0,0,0,0,0,0,0,0,0,0]"
  elif direction=="NONE":
    iconnumber="[0,0,0,63390,63390,0,0,0,0,0,63390,0,0,63390,0,0,0,0,0,0,0,63390,0,0,0,0,0,0,63390,0,0,0,0,0,0,63390,0,0,0,0,0,0,0,63390,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63390,0,0,0,0]"   

  # If everything goes well, send all data to  server
  sendGlucose(glucose, r_color, g_color, b_color, iconnumber)
  #print(glucose)
