import psycopg2
import boto3
import json


def create_job_xref():
  try:
    conn_string = "host='warehouse-prod.cfa5bandh8z5.us-east-1.rds.amazonaws.com' dbname='warehouse' user='warehouse' password='' port='5432'"
    conn = psycopg2.connect(conn_string)
    print("Connected!")
    cur = conn.cursor()
    cur.execute('select id, external_id from jobs where account_id = 8 order by created_at desc limit 5')
    rows = cur.fetchall()
    s3_client = boto3.resource('s3')
    for row in rows:
      bucket = 'connector-hub-xref-dev'
      s3_client.Object(bucket, "xref/%s/%s/%s/%s/%s" % ('in', 'account', '480', 'job', row[1])).put(Body=json.dumps([row[0]]))
      s3_client.Object(bucket, "xref/%s/%s/%s/%s/%s" % ('out', 'account', '480', 'job', row[0])).put(Body=json.dumps([row[1]]))
      print(row)
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
      conn.close()


create_job_xref()