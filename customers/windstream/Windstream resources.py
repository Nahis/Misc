from http.client import HTTPSConnection
from base64 import b64encode
import json
import psycopg2

CONN_STR = ""
conn = psycopg2.connect(CONN_STR)
cur = conn.cursor()
sql = "INSERT INTO scratch.resources(id, type, name, email, phone, timezoneiana, status, parentresourceinternalid, supervisor)" \
      " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

offset = 0
url = '/rest/ofscCore/v1/resources?offset='
c = HTTPSConnection("api.etadirect.com")
userAndPass = b64encode(b":").decode("ascii")
headers = { 'Authorization' : 'Basic %s' %  userAndPass }
c.request('GET', (url+ '%s') % offset, headers=headers)
res = c.getresponse()
r = res.read().decode('utf8')
data = json.loads(r)
items = data['items']
while items:
    items = data['items']
    offset += 10
    insert_values = []
    for i in items:
        if 'resourceId' in i and (i['resourceType'] == 'PR' or i['resourceType'] == 'T2'):
            row = [i['resourceId'], i['resourceType'], i['name'], i['email'] if 'email' in i else None,
                   i['phone'] if 'phone' in i else None,
                   i['timeZoneIANA'] if 'timeZoneIANA' in i else None,
                   i['status'] if 'status' in i else None,
                   i['parentResourceInternalId'] if 'parentResourceInternalId' in i else None,
                   i['XP_supervisor'] if 'XP_supervisor' in i else None]
            insert_values.append(row)

    try:
        cur.executemany(sql, insert_values)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print('db error %s' % error)

    c.request('GET', (url+ '%s') % offset, headers=headers)
    res = c.getresponse()
    r = res.read().decode('utf8')
    data = json.loads(r)
    items = data['items'] if 'items' in data else None
    print(offset)

if conn is not None:
    conn.close()