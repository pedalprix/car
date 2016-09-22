#! /bin/bash

while true
do
	DATE=`date +%Y-%m-%d:%H:%M:%S`
	echo "PedalPrix: Checking for update at " + $(date)
    git fetch origin master
	reslog=$(git log HEAD..origin/master --oneline)
	if [[ "${reslog}" != "" ]] ; then
		echo "PedalPrix: Change Found!"
		echo "PedalPrix: Rebooting"
		reboot now
   	sleep 30
done
