# This simulates jobs that are received from the Enterprise into Dispatch.
# You will subsequently pick these up and process into your environment.

import requests
import binascii
import hmac
import hashlib
import gzip

# The public key/secret in this section simulates what the keys given to the enterprise
# (i.e. these are just for setting up test data). Therefore, please leave these as they are

#secret_key = 'fa225b48285bbc1700dc933edd68b1e2bc834ff9325b8f8dbac1126a6652db70'
#headers = {
#    'Content-Type': 'application/json',
#    'X-Dispatch-Key': 'account|110|noop'
#}

env = '-sbx'
#secret_key = '0ef69a9b62125c1d04ab43535eac377bcdd2b68815e484c501be461eafd4ba71'  #480 DEV
secret_key = 'fa225b48285bbc1700dc933edd68b1e2bc834ff9325b8f8dbac1126a6652db70'   #110 SBX
headers = {
    'Content-Type': 'application/json',
    'X-Dispatch-Key': 'account|110|noop'
}


# Please note:
# 1. Use the <external_organization_id> that we provide you in the introductory email
# 2. Make sure to change the <external_id> for every run. If you don't and run again, it will
#    update rather than insert a new record
payload = r"""
[
    {
        "header":{
            "record_type": "job",
            "version": "v3"
        },
        "record":{
            "external_ids": ["dispatchme_1226_7"],
            "external_organization_id": "epass",
            "title": "Priority: TEST Dispatch TEST - Standard | Model Name: 24\" UNDERCOUNTER REFRIGERATOR, RIGHT HINGE",
            "description": "**Product Serial Number:** 2464376\n\n**Product Model Number:** UC-24R-RH\n\n**Product Model Name:** 24\" UNDERCOUNTER REFRIGERATOR, RIGHT HINGE\n\n**Problem Description:** THIS IS A DM TEST.\n\n**KB Article:** https://km.subzero.com/advisor/showcase?project=Sub-Zero&case=K29130342\n\n**Special Authorization:** http://service.subzero.com/specialauthentry/createinternal/?ticketnumber=004-00-9004007\n\n**Unit History:** http://service.subzero.com/Tools/UnitHistory?SerialNumber=2464376\n\n**Product Full Warranty:** 2019-06-05\n\n**Product Parts Warranty**: 2029-06-05\n\n**Product SS Warranty**: 2022-06-05\n\n**ASKO Article Number**: \n\n**Installer**: \n\n**Sub-Zero Ticket ID**: test-ud-13012\n\n",
            "service_instructions": "Internal servoce instructions",
            "service_fee": 400,
            "equipment_descriptions": [
                {
                    "manufacturer": "Sub-Zero Freezer Company",
                    "model_number": "UC-24R-RH",
                    "model_name": "some model",
                    "serial_number": "2464376",
                    "installation_date": "2017-06-05",
                    "equipment_type": "Undercounter 24",
                    "location": "Roof 2 Story",
                    "problem": "Air Conditioning (Central-Electric)",
                    "symptom": "NOT WORKING,Not Cooling",
                    "custom_fields": {
                        "age": "11-15 Years",
                        "size": "3.0 Tons",
                        "other": "R22/10 SEER",
                        "style": "Split-Air Cooled",
                        "how_many": "2.",
                        "area_of_home": "Whole House",
                        "manufacturer_warranty": "No"
                    }                    
                }
            ],
            "symptom": "Door won't open",            
            "status": "offered",
            "address":{
                "postal_code": "01235",
                "city": "Boston",
                "state": "MA",
                "street_1": "122 Summer St",
                "street_2": "apt 1"
            },
            "service_type": "plumber",
            "customer": {
                "first_name": "Mitch",
                "last_name": "Davis",
                "external_id": "walkabout_mitchdavis",
                "email": "devs+mitchdavis@dispatch.me",
                "phone_numbers":[
                   {
                      "number":"5552312325",
                      "type":"mobile",
                      "primary":true
                   }
                ],
                "home_address": {
                        "street_1": "72613 Porsche Street",
                        "city": "Revere",
                        "state": "MA",
                        "postal_code": "02151"
                }
            },
             "marketing_attributions": [
              {
                "content": "bingo",
                "campaign": "mamba",
                "source": "orca",
                "term": "glitter",
                "media": "twitter"
              }
            ]
        }
    }
]
"""

payload = gzip.compress(payload.encode())
secret_key = bytearray.fromhex(secret_key)
digester = hmac.new(secret_key, payload, hashlib.sha256)
headers['X-Dispatch-Signature'] = binascii.hexlify(digester.digest()).decode('utf-8')
post = requests.post('https://connect%s.dispatch.me/agent/in' % env, headers=headers, data=payload)
x = 1