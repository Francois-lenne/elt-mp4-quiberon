from model import analyze_video_for_persons
import pandas as pd
# Path to your MP4 video
video_path = "downloaded_video_2024-09-29_10_34.mp4"

# Analyze the video
results = analyze_video_for_persons(video_path)



# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame.from_dict(results, orient='index').reset_index()

# Rename the columns
df.columns = ['frame', 'person_present']

# Display the DataFrame
print(df)