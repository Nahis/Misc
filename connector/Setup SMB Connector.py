# Use this to setup an org for the BMS testing. Make sure to fill in the payload before posting

import requests
import binascii
import hmac
import hashlib
import gzip
import uuid
import json

def make_hub_signed_post_request(public_key, secret_key, uri, body=None, headers={}):
    #body = body.encode('utf-8')
    body = gzip.compress(body.encode())   #gzip

    secret_key = bytearray.fromhex(secret_key)  # translate key from hex to bytes
    signature = get_signature(secret_key, body)
    print(signature)
    headers['X-Dispatch-Key'] = public_key
    headers['X-Dispatch-Signature'] = signature
    post = requests.post(uri, headers=headers, data=body)
    print(post.text)

def get_signature(key, body):
    digester = hmac.new(key, body, hashlib.sha256)
    return binascii.hexlify(digester.digest()).decode('utf-8')

## Set these up once
headers = {'Content-Type':'application/json'}
#headers['RecordType'] = 'job'  # specify record type you are working with. This should correlate with the lambda_function.xform_handlers
env = '-sbx'
public_key = 'account|110|noop'
secret_key = 'fa225b48285bbc1700dc933edd68b1e2bc834ff9325b8f8dbac1126a6652db70'

payload = r"""
[
	{
	  "header": {
	    "record_type": "organization",
	    "version": "v3"
	  },
	  "record": {
		  "name" : "<Name of BMS>",
		  "email" : "<bms_email>",
		  "external_id": "<bms_external_id>",
		  "phone_number" : "<bms_phone>",
		  "address": {
		        "street_1": "3310 Maple Avenue",
		        "postal_code": "90731",
		        "city": "San Pedro",
		        "state": "CA"
		 }
	  }
	}
]
"""
make_hub_signed_post_request(public_key,secret_key,'https://connect%s.dispatch.me/agent/in' % env,payload,headers)