from __future__ import print_function
import urllib

def lambda_handler(event, context):
    print("Received event: " + str(event))
    pin = event['Digits']
    
    if pin == '5555':
        return twiliofy('Transferencia completada.')
    else:
        return twiliofy('PIN equivocado. Transferencia no completada.')

              
def twiliofy(input):
    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
           '<Response><Sms>{}</Sms></Response>'.format(input)
