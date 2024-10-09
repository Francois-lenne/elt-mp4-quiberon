from model import analyze_video_for_persons
import pandas as pd
from google.cloud import bigquery
from google.auth import default
from google.cloud import storage
from google.auth import default






# Path to your MP4 video
video_path = "downloaded_video_2024-09-29_10_34.mp4"






# Analyze the video
def retrieve_person_frame(video_path):
    # Analyze the video
    results = analyze_video_for_persons(video_path)

    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame.from_dict(results, orient='index').reset_index()

    df.columns = ['frame', 'person_present']

    df['video_path'] = video_path

    df['day'] = video_path.split("_")[-3]

    df['hour'] = video_path.split("_")[-2] + "_" + video_path.split("_")[-1].split(".")[0]

    df['hour'] = df['hour'].str.replace('_', 'h')



    return df


df_video = retrieve_person_frame(video_path)



# Get the project ID
credentials, project_id = default()


# Define your bucket name
bucket_name = "your-bucket-name"


# Retrieve all file names and paths from the bucket
def list_files_in_bucket(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()

    files = []
    for blob in blobs:
        files.append(blob.name)
        print(blob.name)

    return files


# List all files in the bucket
files = list_files_in_bucket(bucket_name)
print(f"Total files: {len(files)}")


# Load DataFrame into BigQuery
def load_dataframe_to_bigquery(df, table_id):
    client = bigquery.Client()
    job = client.insert_rows_from_dataframe(df, table_id)
    job.result()  # Wait for the job to complete
    print(f"Loaded {job.output_rows} rows into {table_id}.")





# Define your BigQuery table ID
table_id = f"{project_id}.video_quiberon.named_result_ml_bronze"


# Load DataFrame into BigQuery
load_dataframe_to_bigquery(df_video, table_id)

# Print the DataFrame
print(df_video.head())