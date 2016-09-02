#!/usr/bin/env python
# RFID UDP Tx
#
#
# TODO 

import socket
import json
import time
import RPi.GPIO as GPIO
import datetime

import sys
sys.path.append("/home/pi/SPI-Py/MFRC522-python-mxgxw")
import MFRC522


def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True

# open car_config.json and read
configfile = open('Car-config.json', 'r')
configjson = configfile.read()
configfile.close()
if is_json(configjson): 
  json_data = json.loads(configjson)
else:
  print "ERROR: Car-config.json not valid json"
  sys.exit()

car_name = json_data['Car_Name']

RFID_LOG_IP = json_data['RFID_LOG_IP']
RFID_LOG_PORT = int(json_data['RFID_LOG_PORT'])
RFID_POLL_DELAY = float(json_data['RFID_POLL_DELAY'])

msg_type = "RFID"

RFID_LOG_ADDR = (RFID_LOG_IP, RFID_LOG_PORT)

RFID_Log_Msg_count = 0

def JSON_Header():
   global car_name
   global msg_type
   global RFID_Log_Msg_count
   Header = '{"TimeACST":"' + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
   Header +='","Msg_Count":"'+ str(RFID_Log_Msg_count)
   Header +='","Car_Name":"' + car_name
   Header +='","Msg_Type":"' + msg_type
   Header +='","Msg":['
   return Header

JSON_Footer = ']}'

# open UDP socket to RFID Log server
sRFID_Log = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# send response to RFID log
#RFID_Log_Msg_count += 1
#MESSAGE = JSON_Header() + RFID_msg + JSON_Footer
#sRFID_Log.sendto(MESSAGE, RFID_LOG_ADDR)

try:
   while True:

      # Scan for cards
      (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

      # Get the UID of the card
      (status,uid) = MIFAREReader.MFRC522_Anticoll()

      # If we have the UID, continue
      if status == MIFAREReader.MI_OK:

        RFID_json = '{"RFID-UID":"' + str(uid) + '"}'

        # Create valid JSON and send to RFID log

        RFID_Log_Msg_count += 1
        MESSAGE = JSON_Header() + RFID_json + JSON_Footer
        print "MESSAGE :", MESSAGE
        sRFID_Log.sendto(MESSAGE, RFID_LOG_ADDR)

        # The next two seem to reset/flush the reader
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
      else:
        print "Status : ", status
      time.sleep(RFID_POLL_DELAY)

except:
   print "Exception detected."

finally:
   print "Closing sockets"
   sRFID_Log.close()
   GPIO.cleanup()
   print "Bye"
