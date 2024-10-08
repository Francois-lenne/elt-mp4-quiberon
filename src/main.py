import requests
import datetime
from datetime import timedelta
import time
from google.cloud import storage

def download_and_upload_to_gcs(url, blob_name, bucket_name):
        response = requests.get(url, stream=True)
        if response.status_code == 200:

            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_string(response.content)
            print(f"Video uploaded successfully as {blob_name}")
        else:
            print(f"Failed to download video. Status code: {response.status_code}")




def main(event, context):
    date_formatee = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')
    date_name_formatee = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    print(f"Processing videos for date: {date_formatee}")

    # Record start time
    start_time = time.time()

    # Initialize GCS client
    

    # Specify your bucket name
    bucket_name = "bucket_quiberon_video"
    

    # Generate links with hours and minutes
    for hour in range(10, 18):
        for minute in range(4, 64, 10):
            hour_str = str(hour).zfill(2)
            minute_str = str(minute).zfill(2)
            url = f"https://data.skaping.com/quiberon/video-panoramique/{date_formatee}/{hour_str}-{minute_str}.mp4"
            blob_name = f"videos/{date_name_formatee}/{hour_str}_{minute_str}.mp4"
            download_and_upload_to_gcs(url, blob_name, bucket_name)

    # Record end time
    end_time = time.time()

    # Calculate and display the difference
    execution_time = end_time - start_time
    print(f"Function execution time: {execution_time} seconds.")

# For local testing
if __name__ == "__main__":
    main(None, None)