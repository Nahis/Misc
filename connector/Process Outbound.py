import requests
import binascii
import hmac
import hashlib
import json

MAX_MESSAGES = 10
BODY = ('{"maxNumberOfMessages": %s}' % MAX_MESSAGES).encode('utf-8')
env = '-sbx'
secret_key = '14a8d8616d5d3dfaa249a40ebd2e0317adc70ed1b30ed5cdafc07f165f97fa1b'
headers = {
    'Content-Type':'application/json',
    'X-Dispatch-Key': 'account|107|ax'
}
secret_key = bytearray.fromhex(secret_key)  # translate key from hex to bytes
# Calculate the hash and assign to HTTP header
digester = hmac.new(secret_key, BODY, hashlib.sha256)
headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')
# Post to agent/out
response = requests.post('https://connect%s.dispatch.me/agent/out' % env , headers=headers, data=BODY)
msgs = json.loads(response.text)
while msgs:
    for msg in msgs:
        m = msg['Message']
        ret = 'success'
        err = ''
        try:
            # Retrieve message type and payload
            req_type = m['Request']['Type']
            payload = m['Request']['Payload']
            ##########################################################
            # DO SOMETHING HERE WITH THE PAYLOAD - update your system!
            ##########################################################
        except Exception as e:
            ret = 'error'
            err = str(e)
        finally:
            # After processing the message post acknowledgement
            body = '{"Receipt":"%s","ProcedureID":"%s","Result":"%s","Error":"%s"}' % \
                   (m['Receipt'],m['Request']['ProcedureID'],ret,err)
            body = body.encode('utf-8')
            # Calculate the hash and assign to HTTP header
            digester = hmac.new(secret_key, body, hashlib.sha256)
            headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')
            # Post to agent/ack
            req = requests.post('https://connect%s.dispatch.me/agent/ack' % env, headers=headers, data=body)
            print(req.status_code)

    if len(msgs) == MAX_MESSAGES:
        response = requests.post('https://connect%s.dispatch.me/agent/out' % env , headers=headers, data=BODY)
        msgs = json.loads(response.text)
    else:
        msgs = None