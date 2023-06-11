import requests
import os

# Initialize the upload
init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
headers = {
    'Authorization': 'Bearer {access-token}',
    'Content-Type': 'application/json; charset=utf-8'
}
data = {
    "source_info": {
        "source": "FILE_UPLOAD",
        "video_size": os.path.getsize("{file_path}"),
        "chunk_size" : os.path.getsize("{file_path}"),
        "total_chunk_count": 1
    }
}
response = requests.post(init_url, headers=headers, json=data)

# Check that the request was successful
if response.status_code == 200:
    upload_url = response.json()["data"]["upload_url"]

    # Upload the video
    upload_headers = {
        'Content-Range': f"bytes 0-{os.path.getsize('{file_path}') - 1}/{os.path.getsize('{file_path}')}",
        'Content-Type': 'video/mp4'
    }
    with open('{file_path}', 'rb') as f:
        upload_response = requests.put(upload_url, headers=upload_headers, data=f)

        # Check that the upload was successful
        if upload_response.status_code == 200:
            print("Video uploaded successfully!")
        else:
            print("Video upload failed.")
else:
    print("Initialization failed.")