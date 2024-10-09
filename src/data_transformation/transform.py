from model import analyze_video_for_persons
import pandas as pd
from google.cloud import bigquery
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



# Load DataFrame into BigQuery
def load_dataframe_to_bigquery(df, table_id):
    client = bigquery.Client()
    job = client.load_table_from_dataframe(df, table_id)
    job.result()  # Wait for the job to complete
    print(f"Loaded {job.output_rows} rows into {table_id}.")



# Get the project ID
credentials, project_id = default()

# Define your BigQuery table ID
table_id = f"{project_id}.video_quiberon.named_result_ml_bronze"


# Load DataFrame into BigQuery
load_dataframe_to_bigquery(df_video, table_id)

# Print the DataFrame
print(df_video.head())