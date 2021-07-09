#!/bin/bash

cd ~/projects/door
source env/bin/activate

fuser -k 5000/tcp #kills previous flask servers running on port 5000
python garage.py &
killall ngrok #only allowed one ngrok tunnel at a time with free license
sleep 3

#wait for internet connection before creating ngrok tunnel
while ! ping -q -w1 -c1 google.com &>/dev/null; do
  sleep 1
  echo 'Waiting for internet connection...'
done
./ngrok http 5000 -log=stdout > ngrok_output.txt &
sleep 1

python url_extractor.py


