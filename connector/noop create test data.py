import requests
import binascii
import hmac
import hashlib
import gzip

secret_key = 'fa225b48285bbc1700dc933edd68b1e2bc834ff9325b8f8dbac1126a6652db70'
headers = {
    'Content-Type': 'application/json',
    'X-Dispatch-Key': 'account|110|noop'
}

payload = r"""
[
    {
        "header":{
            "record_type": "job",
            "version": "v3"
        },
        "record":{
            "external_organization_id": "dispatchme",
            "title": "Test 621 01",
            "status": "offered",
            "description": "some description",
            "external_ids": ["dispatchme_62101"],
            "address":{
                "postal_code": "01235",
                "city": "Boston",
                "state": "MA",
                "street_1": "122 Summer St",
                "street_2": "apt 1"
            },
            "customer_id": 155907,
            "service_type": "plumber"
        }
    }
]
"""
# Change external_id to a new value before posting to create a new job

payload = gzip.compress(payload.encode())   # It is necessary to gzip before sending
secret_key = bytearray.fromhex(secret_key)  # Translate key from hex to bytes
# Calculate the hash and assign to HTTP header
digester = hmac.new(secret_key, payload, hashlib.sha256)
headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')
# Post to agent/in
post = requests.post('https://connect-sbx.dispatch.me/agent/in', headers=headers, data=payload)