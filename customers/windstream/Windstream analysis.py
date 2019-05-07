import psycopg2
import boto3
import json
import gzip
from http.client import HTTPSConnection
from base64 import b64encode

BUCKET = 'connector-hub-in-arch-sbx'
START_FROM_KEY = ''
url = '/rest/ofscCore/v1/activities/'
c = HTTPSConnection("api.etadirect.com")
userAndPass = b64encode(b":").decode("ascii")
headers = { 'Authorization' : 'Basic %s' %  userAndPass }
CONN_STR = ""
conn = psycopg2.connect(CONN_STR)
cur = conn.cursor()


def iterate_bucket_items(prefix):
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=BUCKET, Prefix=prefix)
    for page in page_iterator:
        for item in page['Contents']:
            yield item

def insert_db(prefix):
    sql = "INSERT INTO scratch.windstream_events(id, type, time, user_id, changes, details, resource_id, change_remedy_status, change_activity_workskills, " \
          "status, subscription, change_resource_id, change_time, s3_key, remedy_number, payload)" \
          " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


    s3 = boto3.resource('s3')
    for i in iterate_bucket_items(prefix=prefix):
        if i['Key'] > START_FROM_KEY:
            if 'account/122' in i['Key']:
                print(i['Key'])
                insert_values = []
                j = extract_and_read(s3, BUCKET, i['Key'], 'temp')
                j = json.loads(j)
                try:
                    for r in j:
                        event_type = r['eventType']
                        recId = None
                        changes = None
                        details = None
                        resourceId = None
                        chg_remedy_status = None
                        chg_activity_workskills = None
                        chg_resource_id = None
                        chg_date = None
                        status = None
                        subscription = None
                        if True:
                            try:
                                if event_type.startswith('activity') or event_type == 'customerRequestCreated':
                                    subscription = 'activity'
                                    recId = r['activityDetails']['activityId']
                                    resourceId = r['activityDetails']['resourceId']
                                    status = r['activityChanges']['status'] if 'status' in r['activityChanges'] else None
                                    chg_remedy_status = r['activityChanges']['XA_REMEDY_ACTIVITY_STATUS'] if 'XA_REMEDY_ACTIVITY_STATUS' in r['activityChanges'] else None
                                    changes = json.dumps(r['activityChanges'] if 'activityChanges' in r else None)
                                    details = json.dumps(r['activityDetails'] if 'activityDetails' in r else None)
                                    chg_activity_workskills = r['activityChanges']['XA_activity_workskills_dup'] if 'XA_activity_workskills_dup' in r['activityChanges'] else None
                                    chg_resource_id = r['activityChanges']['resourceId'] if 'resourceId' in r['activityChanges'] else None
                                    chg_date = r['activityChanges']['date'] if 'date' in r['activityChanges'] else None
                                    c.request('GET', (url+ '%s') % recId, headers=headers)
                                    payload = c.getresponse().read().decode('utf8')
                                    activity = json.loads(payload)
                                    remedy_number = activity['XA_Remedy_incident_Nbr'] if 'XA_Remedy_incident_Nbr' in activity else None


                                elif event_type.startswith('resource'):
                                    subscription = 'resource'
                                    recId = r['resourceDetails']['resourceId']
                                    changes = json.dumps(r['resourceChanges'])
                            except:
                                pass

                            if resourceId[0:1] == "e":
                                try:
                                    row = [recId, event_type, r['time'], r['user'], changes, details, resourceId, chg_remedy_status,
                                           chg_activity_workskills, status, subscription, chg_resource_id, chg_date,
                                           i['Key'], remedy_number, payload]
                                    insert_values.append(row)
                                except:
                                    pass
                except:
                    pass
                try:
                    cur.executemany(sql, insert_values)
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
            else:
                print(i['Key'])

def extract_and_read(s3, s3_bucket, key_in, temp_filename=None):
    if temp_filename is None:
        temp_filename = get_temp_filename(key_in)
    s3.Bucket(s3_bucket).download_file(key_in, temp_filename)
    try:
        with gzip.open(temp_filename, 'rb') as f:
            data = f.read().decode('utf-8')
    except:
        f = open(temp_filename, 'r')
        data = f.read()
    return data

insert_db('0.0.1/hydrate/1.0.0/2019/04/12')



if conn is not None:
    conn.close()