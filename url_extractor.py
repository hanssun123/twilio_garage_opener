import os
from twilio.rest import Client

'''
Extracts public URL from ngrok output file and texts it
to user to update webhook in Twilio Console
'''

url = ''

with open('ngrok_output.txt') as f:
    for line in f:
        index = line.find('url')
        if index != -1:
            url = line[index+4:len(line)-1] + '/voice' #get rid of 'url=' and \n at end, and add /voice route
            break
        url = None #no url was found in the file
    
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
user_phone = os.environ['USER_PHONE']
twilio_phone = os.environ['TWILIO_PHONE']
twilio_console_url = os.environ['TWILIO_CONSOLE_URL']

if url == None:
    text_body = 'Error occurred in parsing ngrok output'
else:
    text_body = 'RPi rebooted. Please update Twilio webhook here: ' \
                + twilio_console_url + '\n\n' \
                + 'The new webhook url is: \n' + url
                
message = client.messages.create(
                                    body=text_body,
                                    from_=twilio_phone,
                                    to=user_phone
                                )

#print(message.sid)

    
    