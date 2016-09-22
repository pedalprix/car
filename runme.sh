#! /bin/bash
#
# This bash script is called from .bashrc after the car performs "git pull origin master from "

echo "PedalPrix: Start runme.sh"

echo "Waiting for connection"
while ! ping -c1 www.google.com &>/dev/null; do sleep 2; done

echo "Checking for git change"
git fetch origin
reslog=$(git log HEAD..origin/master --oneline)
if [[ "${reslog}" != "" ]] ; then
	echo "Change Found!"
	echo "Rebooting"
	reboot now

# Start the python scripts
echo "PedalPrix: Starting Car-TxUDP-GPS.py in background"
python Car-TxUDP-GPS.py > GPS.log &
echo "PedalPrix: Starting Car-TxUDP-RFID.py in background"
python Car-TxUDP-RFID.py >RFID.log &
ps
echo "PedalPrix: Finish runme.sh"
