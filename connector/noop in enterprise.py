# This simulates jobs that are received from the Enterprise into Dispatch.
# You will subsequently pick these up and process into your environment.

import requests
import binascii
import hmac
import hashlib
import gzip

# The public key/secret in this section simulates what the keys given to the enterprise
# (i.e. these are just for setting up test data). Therefore, please leave these as they are
secret_key = 'fa225b48285bbc1700dc933edd68b1e2bc834ff9325b8f8dbac1126a6652db70'
headers = {
    'Content-Type': 'application/json',
    'X-Dispatch-Key': 'account|110|noop',
    'RecordType': 'job'
}

# Please note:
# 1. Use the <external_organization_id> that we provide you in the introductory email
# 2. Make sure to change the <external_id> for every run. If you don't and run again, it will
#    update rather than insert a new record
payload = '{"test":"one"}'
payload = payload.encode()
payload = gzip.compress(payload)
secret_key = bytearray.fromhex(secret_key)
digester = hmac.new(secret_key, payload, hashlib.sha256)
x = binascii.hexlify(digester.digest()).decode('utf-8')
headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')
post = requests.post('https://connect-sbx.dispatch.me/agent/in', headers=headers, data=payload)
x=1