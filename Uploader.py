import requests
import os
import pandas as pd
from datetime import datetime

# Load the CSV file
df = pd.read_csv('yourfile.csv')  # replace 'yourfile.csv' with your actual CSV file name

# Loop over each row in the CSV file
for index, row in df.iterrows():
    # Fetch the video details from the CSV file
    video_file_name = row['video_file_name']  # replace 'video_file_name' with your actual column name
    tags = row['tags']  # replace 'tags' with your actual column name
    title = row['title']  # replace 'title' with your actual column name
    time = row['time']  # replace 'time' with your actual column name

    video_file_path = os.path.join('{path_to_videos}', video_file_name)

    # Initialize the upload
    init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
    headers = {
        'Authorization': 'Bearer {access-token}',
        'Content-Type': 'application/json; charset=utf-8'
    }
    data = {
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": os.path.getsize(video_file_path),
            "chunk_size" : os.path.getsize(video_file_path),
            "total_chunk_count": 1
        }
    }
    response = requests.post(init_url, headers=headers, json=data)

    # Check that the request was successful
    if response.status_code == 200:
        upload_url = response.json()["data"]["upload_url"]

        # Upload the video
        upload_headers = {
            'Content-Range': f"bytes 0-{os.path.getsize(video_file_path) - 1}/{os.path.getsize(video_file_path)}",
            'Content-Type': 'video/mp4'
        }
        with open(video_file_path, 'rb') as f:
            upload_response = requests.put(upload_url, headers=upload_headers, data=f)

            # Check that the upload was successful
            if upload_response.status_code == 200:
                print(f"Video {video_file_name} uploaded successfully!")
            else:
                print(f"Video upload failed for {video_file_name}.")
    else:
        print("Initialization failed.")
