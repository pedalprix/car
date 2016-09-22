#! /bin/bash

echo "PedalPrix: Start runme.sh"

echo "PedalPrix: Waiting for connection"
while ! ping -c1 www.google.com &>/dev/null; do :; done

echo "PedalPrix: Checking for git change"
git fetch origin master
reslog=$(git log HEAD..origin/master --oneline)
if [[ "${reslog}" != "" ]] ; then
	echo "PedalPrix: Change Found!"
	echo "PedalPrix: Rebooting"
	reboot now
	
# Start the python scripts
echo "PedalPrix: Starting Car-TxUDP-GPS.py in background"
python Car-TxUDP-GPS.py > GPS.log &
echo "PedalPrix: Starting Car-TxUDP-RFID.py in background"
python Car-TxUDP-RFID.py > RFID.log &
echo "PedalPrix: Running updatecheck.sh in background"
python updatecheck.sh > UC.log &
ps
echo "PedalPrix: Finish runme.sh"
