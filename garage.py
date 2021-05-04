import RPi.GPIO as GPIO
import time
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

_gatePin = os.environ["GATE_PIN"]

app = Flask(__name__)

outPin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(outPin, GPIO.OUT)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    resp = VoiceResponse()
    
    gather = Gather(action='/gather')
    gather.say("Enter pin.")
    resp.append(gather)
    
    resp.say("No pin entered. Goodbye.")
    
    return(str(resp))

@app.route("/gather", methods=['GET', 'POST'])
def gather():
    resp = VoiceResponse()
    
    if "Digits" in request.values:
        pinEntered = request.values["Digits"]
        correctPin = (pinEntered == _gatePin)
        
        if correctPin:
            try:
                GPIO.output(outPin, GPIO.HIGH)
                time.sleep(.5)
            finally:
                GPIO.output(outPin, GPIO.LOW)
            return(str(resp))
        else:
            resp.say("Invalid.")
            
    else:
        resp.say("Error")
    
    return str(resp)
   
if __name__ == "__main__":
    try:
        app.run(debug=False)
    finally:
        GPIO.cleanup()
        
