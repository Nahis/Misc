import botocore
import boto3
import gzip

def read_file(s3, s3_bucket, key_in, temp_filename):
    try:
        s3.Bucket(s3_bucket).download_file(key_in, temp_filename)
        try:
            with gzip.open(temp_filename, 'rb') as f:
                data = f.read().decode('utf-8')
        except:
            f = open(temp_filename, 'r')
            data = f.read()
        return data
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

s3 = boto3.resource('s3')
s3_path = 'connector-hub-in-arch-prod/0.0.1/raw/1.0.0/2019/04/03/15/01/custom/crm/1/account/73/job/762f949a-abc2-4c1a-a67d-108a4b6ff6fb'
s3_path = s3_path.split("/",1)
data = read_file(s3, s3_path[0], s3_path[1], 'temp')
print(data)