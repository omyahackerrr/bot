from flask import Flask, request, jsonify
import requests
import boto3
import time

app = Flask(__name__)

ARCHIVE_ACCESS_KEY = "I5K6xwIfiAKWRAJb"
ARCHIVE_SECRET_KEY = "UbmsVuLSrIYFbVFo"

@app.route('/upload', methods=['POST'])
def upload():
    terabox_url = request.json.get('url')
    item_name = request.json.get('item_name', 'upload_' + str(int(time.time())))

    # Simulated direct video URL (replace with real extractor logic)
    direct_url = terabox_url.replace("teraboxlink.com", "teraboxcdn.com") + "/video.mp4"

    response = requests.get(direct_url, stream=True)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch video'}), 400

    s3 = boto3.resource(
        's3',
        endpoint_url='https://s3.us.archive.org',
        aws_access_key_id=ARCHIVE_ACCESS_KEY,
        aws_secret_access_key=ARCHIVE_SECRET_KEY
    )

    bucket = s3.Bucket(item_name)
    bucket.upload_fileobj(response.raw, 'video.mp4')

    archive_link = f"https://archive.org/details/{item_name}"
    return jsonify({'status': 'Upload complete', 'link': archive_link})
