from hasher import get_video_hash, get_video_hash_from_local_file
from helper import get_video_hash_from_local_file, get_video_hash_from_s3_file, get_image_hash_from_local_file, get_image_hash_from_s3_file, get_audio_hash_from_local_file, get_audio_hash_from_s3_file

# extract_and_save_keyframes('./tmp/cf5ddef9-4aea-4439-a318-4cdeea8a151b.mp4', 1, './results')

# get_video_hash(bucketName='tattle-media', fileName='4ba9454b-398a-4dcc-b8c1-2309979fb3fb.mp4', filePath='test-data/videos/')
# get_video_hash(bucketName='tattle-media', fileName='8a53bfe0-ebee-48b4-962f-d6aeda191c14.mp4', filePath='test-data/videos/',)

# 30s file
# get_video_hash(bucketName='tattle-media', fileName='cf5ddef9-4aea-4439-a318-4cdeea8a151b.mp4', filePath='test-data/videos/')

# hash_value, state = get_video_hash_from_local_file('cf5ddef9-4aea-4439-a318-4cdeea8a151b.mp4')

# hash_value = get_video_hash_from_local_file('da0bd67a-be48-41d0-b730-e72e6aebc702.mp4')
# hash_value = get_video_hash_from_local_file('zoom_0.mp4')

# hash_value = get_video_hash_from_s3_file('4ba9454b-398a-4dcc-b8c1-2309979fb3fb.mp4', 'tattle-media' ,'test-data/videos/')
# hash_value, state = get_video_hash_from_local_file('4ba9454b-398a-4dcc-b8c1-2309979fb3fb.mp4')
# hash_value, state = get_image_hash_from_local_file, get_image_hash_from_s3_file
# result =  get_image_hash_from_s3_file('004e0126-2ef6-41de-97be-e0b9daaee480.jpeg', 'tattle-media', 'test-data/images/')
# result =  get_image_hash_from_local_file('004e0126-2ef6-41de-97be-e0b9daaee480.jpeg')

# result =  get_audio_hash_from_local_file('audio_1.mp3')


result =  get_audio_hash_from_s3_file('audio_1.mp3', 'tattle-media', 'test-data/audios/')
# result =  get_image_hash_from_s3_file('004e0126-2ef6-41de-97be-e0b9daaee480.jpeg', 'tattle-media', 'test-data/images/')
# result = get_video_hash_from_s3_file('4ba9454b-398a-4dcc-b8c1-2309979fb3fb.mp4', 'tattle-media' ,'test-data/videos/')
print(result)
