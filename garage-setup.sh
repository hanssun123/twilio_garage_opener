#!/bin/bash

echo 'initd has run' > /home/pi/projects/door/initd_test.txt

source /home/pi/projects/door/env/bin/activate

killall garage.py
fuser -k 5000/tcp #kills previous flask servers running on port 5000
python /home/pi/projects/door/garage.py &
killall ngrok #only allowed one ngrok tunnel at a time with free license
sleep 3

#wait for internet connection before creating ngrok tunnel
while ! ping -q -w1 -c1 google.com &>/dev/null; do
  sleep 1
  echo 'Waiting for internet connection...'
done
/home/pi/projects/door/./ngrok http 5000 -log=stdout > /home/pi/projects/door/ngrok_output.txt &
sleep 2

python /home/pi/projects/door/url_extractor.py

