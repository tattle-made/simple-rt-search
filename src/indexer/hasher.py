import urllib.request
import boto3
from helper import compute_video_hash

s3 = boto3.client('s3')


def get_video_hash(fileNameInS3):
    with open('./tmp/'+fileNameInS3, 'wb') as f:
        s3.download_fileobj(
            'tattle-media', 'test-data/videos/'+fileNameInS3, f)

    video_hash = compute_video_hash('./tmp/'+fileNameInS3)
    print(video_hash)
