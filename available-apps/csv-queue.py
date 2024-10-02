#!/usr/bin/python3
# -*- coding: utf-8 -*-

## what is csv-queue?
# csv-queue writes Messages to a single csv file (like a database).
# When you don't add an argument to the call csv-queue goes into read mode and
# reads the first item from the queue, sending it to your pixelit and removing
# the first entry.
#
## How to use csv-queue?
#
### write to queue:
# `python3 csv-queue.py "My item to store"`
#
### Read from queue and send it to pixelit:
# `python csv-queue` without argument


# Import pixelit related libs and config from parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixelit
import config
import csv
import inspect

# config:
csvfilename='.csvqueue.csv'

abs_path = os.path.abspath((inspect.stack()[0])[1])
path = os.path.dirname(abs_path)
csvfilename=path+'/'+csvfilename

print(csvfilename)
filesizelimit=3000000 #roughly 3MB

def existscheck():
  if os.path.isfile(csvfilename):
    #print("file exists")
    return 1
  else:
    #print("file does not exists")
    return 0

def empty():
  if os.stat(csvfilename).st_size == 0: 
    #print("File", csvfilename, "is empty.") 
    return 1
  else: 
    return 0


def writetocsv(newData):
  # write newData to local csv file
  print("[Info] Writing",str(newData),"to CSV")
  if existscheck():
    print("filesize", os.stat(csvfilename).st_size,"byte")
    if os.stat(csvfilename).st_size < filesizelimit: #
      with open(csvfilename, 'a', newline='') as csvfile:
        output = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        output.writerow([newData])
    else:
      print("[ERROR] Filesize too large ("+str(os.stat(csvfilename).st_size),"byte)")
      quit()
  else:
    #TODO remove duplicate code --->
    with open(csvfilename, 'a', newline='') as csvfile: 
      output = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      output.writerow([newData])
    

def deletefirstfromcsv():
  with open(csvfilename, "r") as f:
      data = f.read().split("\n")
  del data[0] # Remove the 1st line
  # Save the data
  with open(csvfilename, "w") as f:
      f.write("\n".join(data))

def printallcsv():
  # read first entry from csv file and delete it
  if existscheck():
    print("[Info] All content of CSV")
    with open(csvfilename, newline='') as f:
      reader = csv.reader(f, quotechar='|')
      for row in reader:
        print(row[0])

def readfirstfromcsv():
  # read first entry from csv file and delete it
  if existscheck():
    #print("[Info] Reading from CSV")
    if not empty():
      with open(csvfilename, newline='') as f:
        reader = csv.reader(f, quotechar='|')
        row1 = next(reader)
      deletefirstfromcsv()
      return(row1[0])
    else: 
      # do nothing
      pixelit.skipApp()
      quit()
  else:
    # do nothing
    pixelit.skipApp()
    quit()


def send2matrix(myText):
  # send text to matrix
  print("[INFO][CSV-QUEUE] Sending to LED Matrix:",myText)
  pixelit.sendApp(
    text_msg=myText,
    red=255,
    green=255,
    blue=255,  
    icon="[0,0,0,39222,39222,0,0,0,0,0,0,39222,39222,0,0,0,0,0,0,39222,39222,0,0,0,0,0,0,39222,39222,0,0,0,0,0,0,39222,39222,0,0,0,0,0,0,0,0,0,0,0,0,0,0,39222,39222,0,0,0,0,0,0,39222,39222,0,0,0]",
    bigFont="false",
    scrollText="auto", 
    centerText="true",
    )



if __name__ == "__main__":
  myappname="csvqueue"

  #print(len(sys.argv), sys.argv)


  #if argument given, add an item 
  if len(sys.argv) == 2:
    writetocsv(sys.argv[1])
  # or show it first one on matrix
  else:
    send2matrix(readfirstfromcsv())
  #printallcsv()

  