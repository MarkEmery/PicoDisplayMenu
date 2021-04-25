#!/bin/bash

# The following was written for a Linux laptop. It assumes you have flash_nuke and pimoroni-pico-micropython-0.1.1.uf2 in your
# Downloads directory. I've found that a Pico that's been taken to 100% full can have issues. It's easier to wipe and restore.
# rshell makes this very easy.

DIR="/media/`whoami`/RPI-RP2/"
TTY="/dev/ttyACM0"

echo "Looking for $DIR"
if [[ ! -d $DIR ]]
then
	echo "Please powercycle the Pi Pico with the BOOTSEL button held down."
	sleep 1
fi

while [[ ! -d $DIR ]]
do
	echo -n "."
	sleep 1
done

echo; echo "Copying flash_nuke.uf2"
cp /home/`whoami`/Downloads/flash_nuke.uf2 /media/`whoami`/RPI-RP2/
sleep 5

echo "Waiting for $DIR to reappear"

while [[ ! -d $DIR ]]
do
	echo -n "."
	sleep 1
done

echo; echo "Copying pimoroni-pico-micropython-0.1.1.uf2"

cp /home/`whoami`/Downloads/pimoroni-pico-micropython-0.1.1.uf2 /media/`whoami`/RPI-RP2/
sleep 5

echo -n "Waiting for $TTY "

while [[ ! -c $TTY ]]
do
	echo -n "."
	sleep 1
done
sleep 5

echo; echo "Running rsync to push files."
rshell -f rsync.cmd

