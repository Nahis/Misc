import psycopg2
import boto3
import gzip
from datetime import timedelta, date

START_DT = date(2019, 4, 15)
END_DT = date(2019, 5, 6)
FILTER_ENTITY = 'organization'
FILTER_ID = '56355'
BUCKET = 'connector-hub-in-arch-sbx'
CONN_STR = ""
conn = psycopg2.connect(CONN_STR)
cur = conn.cursor()
SQL = "INSERT INTO scratch.archive_analysis(entity, id, payload, s3_key)" \
      " VALUES(%s, %s, %s, %s)"

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def iterate_bucket_items(prefix):
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=BUCKET, Prefix=prefix)
    for page in page_iterator:
        for item in page['Contents']:
            yield item

def insert_db(prefix):
    s3 = boto3.resource('s3')
    for i in iterate_bucket_items(prefix=prefix):
        insert_values = []
        if FILTER_ENTITY + "/" + FILTER_ID in i['Key']:
            print(i['Key'])
            j = extract_and_read(s3, BUCKET, i['Key'], 'temp')
            try:
                row = [FILTER_ENTITY, FILTER_ID, j, i['Key']]
                insert_values.append(row)
            except:
                pass
        try:
            cur.executemany(SQL, insert_values)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

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

for dt in daterange(START_DT, END_DT):
    dt = dt.strftime("%Y/%m/%d")
    print(dt)
    insert_db('0.0.1/raw/1.0.0/%s' % dt)

if conn is not None:
    conn.close()