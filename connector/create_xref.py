import psycopg2
import boto3
import json

BUCKET = 'connector-hub-xref-dev'
CONN_STR = "host='warehouse-prod.cfa5bandh8z5.us-east-1.rds.amazonaws.com' dbname='warehouse' user='warehouse' password='pAycEOkc^Q88!1fI' port='5432'"
ACCOUNT_ID = 480

def create_job_xref():
  try:
    conn = psycopg2.connect(CONN_STR)
    print("Connected!")
    cur = conn.cursor()
    cur.execute('select id, external_id from jobs where account_id = %s order by created_at desc limit 5' % ACCOUNT_ID)
    rows = cur.fetchall()
    s3_client = boto3.resource('s3')
    for row in rows:
      s3_client.Object(BUCKET, "xref/%s/%s/%s/%s/%s" % ('in', 'account', ACCOUNT_ID, 'job', row[1])).put(Body=json.dumps([row[0]]))
      s3_client.Object(BUCKET, "xref/%s/%s/%s/%s/%s" % ('out', 'account', ACCOUNT_ID, 'job', row[0])).put(Body=json.dumps([row[1]]))
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
      conn.close()


create_job_xref()