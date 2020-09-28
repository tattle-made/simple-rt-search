import sys,os,json
from dotenv import load_dotenv
load_dotenv()
import requests
import logging
import re


def get_data(record):
    data = {}
    data["file_url"] = record["s3_url"]
    data["media_type"] = record["media_type"]
    data["bucket_name"] = "sharechat-scraper.tattle.co.in"
    data["filepath_prefix"] = ""
    if record["media_type"] == "video":
        data["file_name"] = record["filename"] + ".mp4"
    elif record["media_type"] == "image":
        data["file_name"]= record["filename"] + ".jpg"
    data["metadata"] = {"source": "sharechat", "source_id": str(record["_id"])}
    return json.dumps(data)

def index_media(data):
    url = "http://localhost:5000/media"
    headers= {"content-type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=data)
    return response.text