from __future__ import print_function
import urllib
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

def lambda_handler(event, context):
    # Debug prints
    # print("Received event: " + str(event))
    
    action = event['Body'].split('+')
    caller = urllib.parse.unquote(event['From'])
    
    # Debug prints
    # print(caller)
    # print(action)

    if action[0].lower() == 'saldo':
        return twiliofy('Hola! Tienes -S/500.00 en tu cuenta.')
    elif action[0].lower() == 'transferir':
        amount = action[1]
        account = urllib.parse.unquote(action[2])
        if float(amount) > 250.0:
            return twiliofy('Perdón pero no se puede mandar más de S/250.00 al día.')
        elif float(amount) > 100.0:
            account_sid = os.environ.get('ACCOUNT_SID')
            auth_token = os.environ.get('AUTH_TOKEN')
            client = Client(account_sid, auth_token)

            call = client.calls.create(
                        twiml='<?xml version="1.0" encoding="UTF-8"?><Response><Gather input="dtmf" timeout="10" numDigits="4" action="https://g39fqy6qhf.execute-api.ca-central-1.amazonaws.com/test/verify" method="POST"><Say voice="alice" language="es-MX">Por favor marque su pin de todosmas para confirmar la transferencia de {} soles a la cuenta {}.</Say></Gather></Response>'.format(amount, account),
                        to=caller,
                        from_='+12029317867'
                    )
            return twiliofy('Procesando transferencia de S/{} a {}.'.format(amount, account))
        else:
            return twiliofy('Has transferido S/{} a {}.'.format(amount, account))

    else:
        return twiliofy('No se que quieres hacer!')
              
def twiliofy(input):
    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
           '<Response><Message><Body>{}</Body></Message></Response>'.format(input)
        
        