import requests
import binascii
import hmac
import hashlib
import json
import boto3

ENV = ''
ENTITY = 'organization'
ENTITY_ID = 1219

s3 = boto3.resource('s3')
FILE_NAME = 'temp'
BUCKET = 'connector-agent-config-%s' % 'prod' if not ENV else 'sbx'
key_in = '0.0.1/%s/%s/noop' % (ENTITY, ENTITY_ID)
s3.Bucket(BUCKET).download_file(key_in, FILE_NAME)
f = open(FILE_NAME, 'r')
data = f.read()
data = json.loads(data)

MAX_MESSAGES = 10
BODY_MAX_MESSAGES = ('{"maxNumberOfMessages": %s}' % MAX_MESSAGES).encode('utf-8')
SECRET_KEY = data['encryption_key']
HEADERS = {
    'Content-Type': 'application/json',
    'X-Dispatch-Key': data['id']
}
b_secret_key = bytearray.fromhex(SECRET_KEY)  # translate key from hex to bytes
digester = hmac.new(b_secret_key, BODY_MAX_MESSAGES, hashlib.sha256)
out_headers = HEADERS
out_headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')
out_response = requests.post('https://connect%s.dispatch.me/agent/out' % ENV, headers=out_headers,
                             data=BODY_MAX_MESSAGES)
msgs = json.loads(out_response.text)
while msgs:
    for msg in msgs:
        try:
            m = msg['Message']
            ret = 'success'
            err = ''
            req_type = m['Request']['Type']
            payload = m['Request']['Payload']
            ack = payload['Actions'][0]['Put']
            print(msg)
            ##########################################################
            # DO SOMETHING HERE WITH THE PAYLOAD - update your system!
            ##########################################################
        except Exception as e:
            ret = 'error'
            err = str(e)
        finally:
            # After processing the message post acknowledgement
            receipt = '{"Receipt":"%s","ProcedureID":"%s","Result":"%s"}' % \
                      (m['Receipt'], m['Request']['ProcedureID'], ret)
            receipt = receipt.encode('utf-8')

            digester = hmac.new(b_secret_key, receipt, hashlib.sha256)
            ack_headers = HEADERS
            ack_headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')
            # Post to agent/ack
            ack_response = requests.post('https://connect%s.dispatch.me/agent/ack' % ENV, headers=ack_headers,
                                         data=receipt)

    if len(msgs) == MAX_MESSAGES:
        digester = hmac.new(b_secret_key, BODY_MAX_MESSAGES, hashlib.sha256)
        out_headers = HEADERS
        out_headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')

        out_response = requests.post('https://connect%s.dispatch.me/agent/out' % ENV, headers=out_headers,
                                     data=BODY_MAX_MESSAGES)
        msgs = json.loads(out_response.text)
    else:
        msgs = None