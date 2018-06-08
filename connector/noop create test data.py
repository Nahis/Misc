import requests
import binascii
import hmac
import hashlib
import gzip

secret_key = 'fa225b48285bbc1700dc933edd68b1e2bc834ff9325b8f8dbac1126a6652db70'
headers = {
    'Content-Type': 'application/json',
    'RecordType': 'job',    # Specify record type you are working with
    'X-Dispatch-Key': 'account|110|noop'
}

# Change external_id to a new value before posting to create a new job
payload = r"""
[
    {
        "header":{
            "record_type": "job",
            "version": "v3"
        },
        "record":{
            "external_organization_id": "walkabout",
            "title": "Fix Ceiling 5",
            "description": "some description",
            "external_ids": ["walkabout_5"],
            "address":{
                "postal_code": "01235",
                "city": "Boston",
                "state": "MA",
                "street_1": "122 Summer St",
                "street_2": "apt 1"
            },
            "customer_id": 155906,
            "service_type": "plumber"
        }
    }
]
"""

payload = gzip.compress(payload.encode())   # It is necessary to gzip before sending
secret_key = bytearray.fromhex(secret_key)  # Translate key from hex to bytes
# Calculate the hash and assign to HTTP header
digester = hmac.new(secret_key, payload, hashlib.sha256)
headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')
# Post to agent/in
post = requests.post('https://connect-sbx.dispatch.me/agent/in', headers=headers, data=payload)