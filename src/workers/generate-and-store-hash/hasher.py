import urllib.request
import boto3
from helper import compute_video_hash

s3 = boto3.client('s3')


def get_video_hash(bucketName, fileName, filePath):
    # with open('./tmp/'+fileName, 'wb') as f:
        # s3.download_fileobj(
            # bucketName, filePath+fileName, f)

    video_hash = compute_video_hash('./tmp/'+fileName)
    print(video_hash)

def get_video_hash_from_local_file(fileName, filePathPrefix):
    video_hash = compute_video_hash_from_local_file(fileName, filePathPrefix)
    print(video_hash)