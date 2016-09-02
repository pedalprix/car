#! /bin/bash
#
# This bash script is called from .bashrc after the car performs "git pull origin master from "

cd ~/car

# Start the python scripts
./python Car-TxUDP-GPS.py &
./python Car-TxUDP-RFID.py &
