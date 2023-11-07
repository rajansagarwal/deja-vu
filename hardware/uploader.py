import os
from google.cloud import storage
import time

def upload_file():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys\hack-the-north-2023-f70ed239b8d8.json"
    client = storage.Client()
    current_time = time.time()
    bucket_name = "hack-the-north-2023"
    source_file_name = "Default_user.avi"
    destination_blob_name = f"audio_{current_time}.avi"
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)