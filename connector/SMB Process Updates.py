import requests
import binascii
import hmac
import hashlib
import gzip

env = '-sbx'
secret_key = 'a09726fbf6bf610fe38773fa9de7140e46d085a30fddad6dc1f6ff9ad3abe692'
headers = {
    'Content-Type': 'application/json',
    'X-Dispatch-Key': 'organization|105509|noop'
}

payload = r"""
    [{
        "header": {
            "record_type": "job",
            "version": "v3"
        },
        "record": {
            "id": 177501,
            "status": "complete",
            "status_message": "Customer canceled"
        }
    }] 
"""

payload = gzip.compress(payload.encode())
secret_key = bytearray.fromhex(secret_key)
digester = hmac.new(secret_key, payload, hashlib.sha256)
headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')
post = requests.post('https://connect%s.dispatch.me/agent/in' % env, headers=headers, data=payload)
x = 1