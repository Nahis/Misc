import psycopg2
import boto3
import json

BUCKET = 'connector-hub-in-arch-stg'
START_FROM_KEY = ''
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
    sql = "INSERT INTO scratch.events(id, type, time, user_id, changes, resource_id, change_remedy_status, change_activity_workskills, " \
          "status, subscription, change_resource_id, change_time, s3_key)" \
          " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    s3 = boto3.resource('s3')
    for i in iterate_bucket_items(prefix=prefix):
        if i['Key'] > START_FROM_KEY:
            insert_values = []
            j = json.loads(s3.Object(BUCKET, i['Key']).get()['Body'].read().decode('utf-8'))
            for r in j['items']:
                event_type = r['eventType']
                recId = None
                changes = None
                resourceId = None
                chg_remedy_status = None
                chg_activity_workskills = None
                chg_resource_id = None
                chg_date = None
                status = None
                subscription = None
                #if event_type not in ['routingRun', 'routeCreated', 'routeUpdated', 'userCreated',
                #                      'userUpdated', 'routeActivated']:
                if True:
                    try:
                        if event_type.startswith('activity') or event_type == 'customerRequestCreated':
                            subscription = 'activity'
                            recId = r['activityDetails']['activityId']
                            resourceId = r['activityDetails']['resourceId']
                            status = r['activityChanges']['status'] if 'status' in r['activityChanges'] else None
                            chg_remedy_status = r['activityChanges']['XA_REMEDY_ACTIVITY_STATUS'] if 'XA_REMEDY_ACTIVITY_STATUS' in r['activityChanges'] else None
                            changes = json.dumps(r['activityChanges'] if 'activityChanges' in r else None)
                            chg_activity_workskills = r['activityChanges']['XA_activity_workskills_dup'] if 'XA_activity_workskills_dup' in r['activityChanges'] else None
                            chg_resource_id = r['activityChanges']['resourceId'] if 'resourceId' in r['activityChanges'] else None
                            chg_date = r['activityChanges']['date'] if 'date' in r['activityChanges'] else None
                        elif event_type.startswith('resource'):
                            subscription = 'resource'
                            recId = r['resourceDetails']['resourceId']
                            changes = json.dumps(r['resourceChanges'])
                    except:
                        pass

                    row = [recId, event_type, r['time'], r['user'], changes, resourceId, chg_remedy_status,
                           chg_activity_workskills, status, subscription, chg_resource_id, chg_date, i['Key']]
                    insert_values.append(row)
            try:
                cur.executemany(sql, insert_values)
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

insert_db('0.0.1/listen/1.0.0/2018/10/11/11')
insert_db('0.0.1/listen/1.0.0/2018/10/11/12')

if conn is not None:
    conn.close()