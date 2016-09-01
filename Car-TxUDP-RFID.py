#!/usr/bin/env python
# RFID UDP Tx

import socket
import json
import time
import RPi.GPIO as GPIO
import MFRC522
import datetime

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

# parse configdata
json_data = json.loads(configjson)
car_name = json_data['Car_Name']

RFID_LOG_IP = json_data['RFID_LOG_IP']
RFID_LOG_PORT = int(json_data['RFID_LOG_PORT'])
RFID_POLL_DELAY = float(json_data['RFID_POLL_DELAY'])

msg_type = "RFID"

RFID_LOG_ADDR = (RFID_LOG_IP, RFID_LOG_PORT)

RFID_Log_Msg_count = 0

def JSON_Header:
   global car_name
   global msg_type
   global RFID_Log_Msg_count
   return = '{"Car_Name":"' + car_name + '","Msg_Type":"' + msg_type + '","Msg_count":"'+ RFID_Log_Msg_count + ',"Msg":['

JSON_Footer = ']}'

# open UDP socket to RFID Log server
sRFID_Log = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# send response to RFID log
RFID_Log_Msg_count += 1
MESSAGE = JSON_Header() + RFID_msg + JSON_Footer
sRFID_Log.sendto(MESSAGE, RFID_LOG_ADDR)

try:
   while True:
      # Scan for cards    
      (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

      # Get the UID of the card
      (status,uid) = MIFAREReader.MFRC522_Anticoll()

      # Get the datetime
      RFIDtime = datetime.now().strftime('%Y-%m-%dT%H.%M.%SZ')

      # If we have the UID, continue
      if status == MIFAREReader.MI_OK:

        # Print UID
        UID_str = "["+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+","+str(uid[4])+","+str(uid[5])+","+str(uid[6])+"]"
	RFID_json = '{"time":"' + RFIDtime + '","RFID-UID":"' + UID_Str + '"}'

      # Create valid JSON and send to RFID log
      RFID_Log_Msg_count += 1
      MESSAGE = JSON_Header() + RFID_json + JSON_Footer
      sRFID_Log.sendto(MESSAGE, RFID_LOG_ADDR)

      time.sleep(RFID_POLL_DELAY)

except:
   print "Exception detected."

finally:
   print "Closing sockets"
   sRFID_Log.close()
   GPIO.cleanup()
   print "Bye"
