import requests
import binascii
import hmac
import hashlib
import gzip

secret_key = 'a09726fbf6bf610fe38773fa9de7140e46d085a30fddad6dc1f6ff9ad3abe692'
headers = {
    'Content-Type': 'application/json',
    'X-Dispatch-Key': 'organization|105509|noop'
}

# Change external_id to a new value before posting to create a new job
payload = r"""
    [{
        "header": {
            "record_type": "job",
            "version": "v3"
        },
        "record": {
            "id": 109110,
            "status": "accepted"
        }
    }]
"""

payload = gzip.compress(payload.encode())   # It is necessary to gzip before sending
secret_key = bytearray.fromhex(secret_key)  # Translate key from hex to bytes
# Calculate the hash and assign to HTTP header
digester = hmac.new(secret_key, payload, hashlib.sha256)
headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')
# Post to agent/in
post = requests.post('https://connect-sbx.dispatch.me/agent/in', headers=headers, data=payload)