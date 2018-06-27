'''
This can be used to post a request to the inbound connect endpoint using HMAC auth.
Just modify the payload as necessary and run.
'''
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
[{
	"header": {
		"record_type": "job",
		"version": "v3"
	},
	"record": {
		"title": "Test job 2",
		"description": "in the basement",
		"external_id": "ext_test_job_2",
		"address": {
			"postal_code": "01234",
			"city": "Boston",
			"state": "MA",
			"street_1": "1214 Summer St",
			"street_2": "apt. 1"
		},
		"service_type": "plumber",
		"customer": {
			"first_name": "Donovan",
			"last_name": "Johnson",
			"external_id": "ext_donovan_johson",
			"email": "devs+donovanjohnson@dispatch.me",
			"phone_numbers": [{
				"number": "+15550983814",
				"primary": true,
				"type": "Mobile"
			}],
			"home_address": {
				"street_1": "3915 Ford Street",
				"city": "Revere",
				"state": "MA",
				"postal_code": "02151"
			}
		},
		"organization": {
			"name": "DispatchMe Testing",
			"email": "devs+dispatchme1@dispatch.me",
			"external_id": "dispatchme",
			"phone_number": "(555)015-4123",
			"address": {
				"street_1": "3316 Maple Avenue",
				"postal_code": "90731",
				"city": "San Pedro",
				"state": "CA"
			}
		}
	}
}]
"""

make_hub_signed_post_request(public_key,secret_key,'https://connect%s.dispatch.me/agent/in' % env,payload,headers)