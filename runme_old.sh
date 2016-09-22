#! /bin/bash

echo "PedalPrix: Start runme.sh"

# Start the python scripts
echo "PedalPrix: Starting Car-TxUDP-GPS.py in background"
python Car-TxUDP-GPS.py > GPS.log &
echo "PedalPrix: Starting Car-TxUDP-RFID.py in background"
python Car-TxUDP-RFID.py > RFID.log &

ps
echo "PedalPrix: Finish runme.sh"
