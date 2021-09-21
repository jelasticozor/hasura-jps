import os

import psycopg2


# TODO: get the uuid out of the req
def handle(req):
    print('req = ', req)

    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME'])
