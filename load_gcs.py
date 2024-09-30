import requests
import datetime
from datetime import timedelta
import time
from google.cloud import storage


date_formatee = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')

date_name_formatee = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


# Enregistrer l'heure de début
start_time = time.time()


# Initialiser le client GCS
storage_client = storage.Client()

    # Spécifier le nom de votre bucket
bucket_name = "bucket_quiberon_video"
bucket = storage_client.bucket(bucket_name)

def download_and_upload_to_gcs(url, blob_name):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            blob = bucket.blob(blob_name)
            blob.upload_from_string(response.content)
            print(f"Video uploaded successfully as {blob_name}")
        else:
            print(f"Failed to download video. Status code: {response.status_code}")

    # Générer les liens avec les heures et les minutes
for hour in range(10, 18):
    for minute in range(4, 64, 10):
            hour_str = str(hour).zfill(2)
            minute_str = str(minute).zfill(2)
            url = f"https://data.skaping.com/quiberon/video-panoramique/{date_formatee}/{hour_str}-{minute_str}.mp4"
            blob_name = f"videos/{date_name_formatee}/{hour_str}_{minute_str}.mp4"
            download_and_upload_to_gcs(url, blob_name)

    # Enregistrer l'heure de fin
    end_time = time.time()

    # Calculer et afficher la différence
    execution_time = end_time - start_time
    print(f"Le temps d'exécution de la fonction est de {execution_time} secondes.")