#!/usr/bin/env python
# GPS UDP Tx

import socket
import json
import time

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

GPSD_INIT_msg = '?WATCH={"enable":true,"json":true}'
GPSD_POLL_msg = '?POLL;'
GPSD_ADDR = (GPSD_IP, GPSD_PORT)
GPS_LOG_ADDR = (GPS_LOG_IP, GPS_LOG_PORT)

GPS_Log_Msg_count = 0

def JSON_Header:
   global car_name
   global msg_type
   global Msg_count
   return = '{"Car_Name":"' + car_name + '","Msg_Type":"' + msg_type + '","Msg_count":"'+ GPS_Log_Msg_count + ',"Msg":['

JSON_Footer = ']}'

# open UDP socket to GPS Log server
sGPS_Log = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# open TCP socket to GPSD server
sGPSD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sGPSD.connect(GPSD_ADDR)

# fetch version info sent to us as a result of connecting
GPSD_json = sGPSD.recv(GPSD_BUFFER_SIZE)
print "== GPSD connecion response follows =="
print GPSD_json

# send response to GPS log
GPS_Log_Msg_count += 1
MESSAGE = JSON_Header() + GPSD_json + JSON_Footer
sGPS_Log.sendto(MESSAGE, GPS_LOG_ADDR)

# Initialise connection with GPSD
sGPSD.send(GPSD_INIT_msg)
GPSD_json = sGPSD.recv(GPSD_BUFFER_SIZE)
print "== GPSD response from sending : ",GPSD_INIT_msg
print GPSD_json

# send response to GPS log
GPS_Log_Msg_count += 1
MESSAGE = JSON_Header() + GPSD_json + JSON_Footer
sGPS_Log.sendto(MESSAGE, GPS_LOG_ADDR)

try:
   while True:
      # Poll the GPSd and get response
      sGPSD.send(GPSD_POLL_msg)
      GPSD_json = sGPSD.recv(GPSD_BUFFER_SIZE)

      if is_json(GPSD_msg): # If it's valid JSON send to GPS log
         GPS_Log_Msg_count += 1
         MESSAGE = JSON_Header() + GPSD_json + JSON_Footer
         sGPS_Log.sendto(MESSAGE, GPS_LOG_ADDR)

      else:
         print "Invalid JSON detected"

      time.sleep(GPS_POLL_DELAY)

except:
   print "Exception detected."

finally:
   print "Closing sockets"
   sGPSD.close()
   sGPS_Log.close()
   print "Bye"
