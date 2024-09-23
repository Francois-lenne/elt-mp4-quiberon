import requests
import datetime
from datetime import timedelta
import time

# Formater la date au format YYYY/MM/DD
date_formatee = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')

date_name_formatee = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


# Enregistrer l'heure de début
start_time = time.time()

# Afficher la date formatée
print(date_formatee)

def download_video(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Video downloaded successfully as {filename}")
    else:
        print(f"Failed to download video. Status code: {response.status_code}")



# Générer les liens avec les heures et les minutes
for hour in range(8, 21):
    for minute in range(4, 64, 10):
        hour_str = str(hour).zfill(2)
        minute_str = str(minute).zfill(2)
        download_video(f"https://data.skaping.com/quiberon/video-panoramique/{date_formatee}/{hour_str}-{minute_str}.mp4", f"downloaded_video_{date_name_formatee}_{hour_str}_{minute_str}.mp4")



# Enregistrer l'heure de fin
end_time = time.time()

# Calculer et afficher la différence
execution_time = end_time - start_time
print(f"Le temps d'exécution du programme est de {execution_time} secondes.")