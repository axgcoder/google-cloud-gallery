from flask import Flask, render_template, request,url_for
import MySQLdb
import logging
import os
from google.cloud import storage
import boto
import gcs_oauth2_boto_plugin
import os
import timeit

from datetime import date, datetime, timedelta

# URI scheme for Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'
project_id = 'instant-duality-202100'

#comment the below code when uploading to linux vm
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sample.json"

app = Flask(__name__)

@app.route('/')
def hello_world():
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
 storage_client = storage.Client()

    # Make an authenticated API request
 buckets = list(storage_client.list_buckets())
 print(buckets)

 #Lists all the blobs in the bucket.
 bucket_name =buckets[0].name
 bucket = storage_client.get_bucket(bucket_name)
 blobs = bucket.list_blobs()

 for blob in blobs:
    print(blob.name)

    db = connectDB()
    #query = "SELECT * FROM project.imagedb limit 1000"
    query= "SELECT COUNT(mag) FROM edata.edata where mag > 5.0"
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    cursor.close()


    return render_template('index.html',data=data)
    #return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def searchdata():
    start_time = timeit.default_timer()
    search = request.form['search']

    cloud_start_time = timeit.default_timer()
    db = connectDB()
    query = "SELECT * FROM project.imagedb where Creator='"+search+"'"
    #FileName LIKE '" '%' +search+ '%'"'"
    cursor = db.cursor()
    cursor.execute(query)
    cloud_finish_time = str(round(timeit.default_timer() - cloud_start_time,4))
    data = cursor.fetchall()
    db.close()
    cursor.close()
    # cursor = connection.cursor()
    finish_time = str(round(timeit.default_timer() - start_time,4))
    return render_template("index.html", data=data,finish_time=finish_time,cloud_finish_time=cloud_finish_time)


def connectDB():
    host = "xx.xxx.xx.xx"
    port = 3306
    dbname = "db"
    user = "username"
    password = "xxxxx"
    try:
     print("connecting")
     db = MySQLdb.connect(host=host,  # your host, usually localhost
                         user=user,  # your username
                         passwd=password,  # your password
                         db=dbname,
                         port=port,
                         charset='utf8',
                         use_unicode=True)
     print("connected to db")
    except Exception:
        print(Exception)
    return db

if __name__ == '__main__':
  app.run()