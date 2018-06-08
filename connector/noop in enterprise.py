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
env = '-dev'
public_key = 'account|480|noop'
secret_key = '0ef69a9b62125c1d04ab43535eac377bcdd2b68815e484c501be461eafd4ba71'

payload = r"""
[{
	"header": {
		"record_type": "job",
		"version": "v3"
	},
	"record": {
		"title": "Test job noop 1014 3",
		"status": "complete",
		"description": "in the basement",
		"external_id": "job_noop14_3",
		"address": {
			"postal_code": "01234",
			"city": "Boston",
			"state": "MA",
			"street_1": "1214 Summer St",
			"street_2": "apt. 1"
		},
		"service_type": "plumber",
		"customer": {
			"first_name": "Marian",
			"last_name": "Noop",
			"external_id": "cust_noop14_1",
			"email": "devs+noop14@dispatch.me",
			"phone_numbers": [{
				"number": "+15550913814",
				"primary": true,
				"type": "Mobile"
			}],
			"home_address": {
				"street_1": "3914 Ford Street",
				"city": "Revere",
				"state": "MA",
				"postal_code": "02151"
			}
		},
		"organization": {
			"name": "Test noop14",
			"email": "devs+noop14@dispatch.me",
			"external_id": "org_noop14",
			"phone_number": "(555)014-0352",

			"address": {
				"street_1": "3314 Maple Avenue",
				"postal_code": "90731",
				"city": "San Pedro",
				"state": "CA"
			}
		},
		"suggested_times": [
		    {
                "start_time": "2018-06-05T17:00:00+0000",
                "end_time": "2018-06-05T19:00:00+0000"
		    },
		    {
                "start_time": "2018-06-06T17:00:00+0000",
                "end_time": "2018-06-06T19:00:00+0000"
		    },
		    {
                "start_time": "2018-06-07T17:00:00+0000",
                "end_time": "2018-06-07T17:00:00+0000"
		    }
		]
	}
}]
"""

make_hub_signed_post_request(public_key,secret_key,'https://connect%s.dispatch.me/agent/in' % env,payload,headers)