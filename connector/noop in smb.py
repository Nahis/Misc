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
public_key = 'organization|11796|noop'
secret_key = '31e4018396b406a22ec5e0646d369d9c8b67c3c4c7a8fa4db709981a1adfaeb2'


'''
payload = r"""
[{
  "header": {
    "record_type": "job",
    "version": "v3"
  },
  "record": {
    "id": 30575,
    "title": "halleyah!!!!",
    "status": "unscheduled"
  }
}]
"""
'''
'''
payload = r"""
[{
  "header": {
    "record_type": "attachment",
    "version": "v3"
  },
  "record": {
    "action": "post",
    "job_id": 30575,
    "description": "tafffassaaanew"
  }
}]
"""
'''

payload = r"""
    [{
		"header": {
			"record_type": "appointment",
			"version": "v3"
		},
		"record": {
		    "action": "post",
			"time": "2018-10-31T22:00:00.000Z",
			"duration": 14400,
			"job_id": 30576,
			"status": "scheduled"
		}
	}]
"""

p1 = json.loads(payload)
make_hub_signed_post_request(public_key,secret_key,'https://connect%s.dispatch.me/agent/in' % env,payload,headers)