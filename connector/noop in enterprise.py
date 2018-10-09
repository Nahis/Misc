# This simulates jobs that are received from the Enterprise into Dispatch.
# You will subsequently pick these up and process into your environment.

import requests
import binascii
import hmac
import hashlib
import gzip

# The public key/secret in this section simulates what the keys given to the enterprise
# (i.e. these are just for setting up test data). Therefore, please leave these as they are
secret_key = 'f0e743efd3a510549251b2fb303b7f42216fce5f2ba35e6e87f35611c1e038f7'
headers = {
    'Content-Type': 'application/json',
    'X-Dispatch-Key': 'account|8|noop'
}

# Please note:
# 1. Use the <external_organization_id> that we provide you in the introductory email
# 2. Make sure to change the <external_id> for every run. If you don't and run again, it will
#    update rather than insert a new record
payload = r"""
[{"header":{"messageID":"0e40a144-c8dd-4554-8061-b6c90624045e","record_type":"user","version":"v3"},"record":{"external_id":"02956","external_organization_id":"HS0001","first_name":"Doherty","last_name":"Michael A.","phone_number":"7182765895","roles":["dispatcher","technician"]}}]
"""

payload = gzip.compress(payload.encode())
secret_key = bytearray.fromhex(secret_key)
digester = hmac.new(secret_key, payload, hashlib.sha256)
headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')
post = requests.post('https://connect.dispatch.me/agent/in', headers=headers, data=payload)