#!/usr/bin/env python
# GPS UDP Tx

import socket
import json
import time
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
GPSD_IP = json_data['GPSD_IP']
GPSD_PORT = int(json_data['GPSD_PORT'])
GPSD_BUFFER_SIZE = int(json_data['GPSD_BUFFER_SIZE'])
GPS_LOG_IP = json_data['GPS_LOG_IP']
GPS_LOG_PORT = int(json_data['GPS_LOG_PORT'])
GPS_POLL_DELAY = float(json_data['GPS_POLL_DELAY'])

msg_type = "GPS"

GPSD_INIT_msg = """?WATCH={"enable":true,"json":true}"""
GPSD_POLL_msg = """?POLL;"""
GPSD_ADDR = (GPSD_IP, GPSD_PORT)
GPS_LOG_ADDR = (GPS_LOG_IP, GPS_LOG_PORT)

GPS_Log_Msg_count = 0

def JSON_Header():
   global car_name
   global msg_type
   global RFID_Log_Msg_count
   Header = '{"TimeACST":"' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   Header +='","Msg_count":"'+ str(GPS_Log_Msg_count)
   Header +='","Car_Name":"' + car_name
   Header +='","Msg_Type":"' + msg_type
   Header +='","Msg":['
   return Header

JSON_Footer = ']}'

# open UDP socket to GPS Log server
sGPS_Log = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# open TCP socket to GPSD server
sGPSD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sGPSD.connect(GPSD_ADDR)

# fetch version info sent to us as a result of connecting
GPSD_json = sGPSD.recv(GPSD_BUFFER_SIZE)

# send response to GPS log
GPS_Log_Msg_count += 1
MESSAGE = JSON_Header() + GPSD_json + JSON_Footer
sGPS_Log.sendto(MESSAGE, GPS_LOG_ADDR)
print "Sending Message received from initial connection to GPSD ==="
print MESSAGE

# Initialise connection with GPSD
sGPSD.send(GPSD_INIT_msg)
GPSD_json = sGPSD.recv(GPSD_BUFFER_SIZE)
GPS_Log_Msg_count += 1
MESSAGE = JSON_Header() + GPSD_json + JSON_Footer
print "Sending Message received from sending : ",GPSD_INIT_msg
print MESSAGE
sGPS_Log.sendto(MESSAGE, GPS_LOG_ADDR)

try:
   while True:
      # Poll the GPSd and get response
      sGPSD.send(GPSD_POLL_msg)
      GPSD_json = sGPSD.recv(GPSD_BUFFER_SIZE)

      if is_json(GPSD_json): # If it's valid JSON send to GPS log
         GPS_Log_Msg_count += 1
         MESSAGE = JSON_Header() + GPSD_json + JSON_Footer
         print "Sending Message ==============================="
         print MESSAGE
         sGPS_Log.sendto(MESSAGE, GPS_LOG_ADDR)
         time.sleep(GPS_POLL_DELAY)

except:
   print "Exception detected."

finally:
   print "Closing sockets"
   sGPSD.close()
   sGPS_Log.close()
   print "Bye"
