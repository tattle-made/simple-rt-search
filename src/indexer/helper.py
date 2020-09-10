# importing required modules
from Katna.video import Video
import timeit
import os
import moviepy.editor
from mp3hash import mp3hash
from PIL import Image
import imagehash
import shutil
import multiprocessing
import cv2
import boto3

s3 = boto3.client('s3')

INPUT_FOLDER = './.input/'
OUTPUT_FOLDER = './.output/'

def create_folder_for_video(path):
    os.makedirs(path)


def get_key_frames_from_video(path_to_video, no_of_frames):
    print('getting key frames from video')
    try:
        video = Video()
        print('begin extraction')
        images = video.extract_frames_as_images(
            no_of_frames=no_of_frames, file_path=path_to_video)
        print('end extraction')
        return images
    except Exception as e:
        print('error getting frames from videos')
        print(e)


def write_images_into_folder(images, no_of_frames, path):
    print('writing images into folder')
    print(no_of_frames)
    print(path)
    try:
        video = Video()
        for i in range(no_of_frames):
            print('saving '+str(i+1)+' frame')
            video.save_frame_to_disk(images[i], file_path=path, file_name="image" + str(i + 1), file_ext=".png")
    except Exception as e:
        print('error saving extracted frames to disk')
        print(e)


def get_audio_from_video(path_to_video):
    video = moviepy.editor.VideoFileClip(path_to_video)
    return video.audio


def write_audio_into_folder(audio, path):
    audio.write_audiofile(path)

def extract_and_save_keyframes(path_to_video, no_of_frames, result_folder_path):
    try:
        vidcap = cv2.VideoCapture(path_to_video)
        vidcap.set(cv2.CAP_PROP_POS_MSEC, 2000)
        success, image = vidcap.read()
        if success:
            cv2.imwrite("./results/image1.jpg", image)
        else:
            print('did not extract frame correctly')
    except Exception as e:
        print('error extracting and saving keyframe')
        print(e)
    # print('extract and save keyframes')
    # try:
        # key_frames = get_key_frames_from_video(path_to_video, no_of_frames)
        # write_images_into_folder(key_frames, no_of_frames, result_folder_path)
    # except:
        # print('error extracting and saving keyframes')


def extract_and_save_audio(path_to_video):
    audio = get_audio_from_video(path_to_video)
    write_audio_into_folder(audio, "./results/audio.mp3")


def hash_image(path_to_image):
    return str(imagehash.average_hash(Image.open(path_to_image)))


def hash_audio(path_to_audio):
    return mp3hash(path_to_audio)


def remove_folder_for_video(path):
    shutil.rmtree(path)


def change_to_be_hex(str):
    return int(str, base=16)


def xor_elements(array):
    acc = 0
    for i in range(len(array)):
        acc = acc ^ change_to_be_hex(array[i])
    return acc


def get_feature_hash_from_video(path_to_video):
    feature_hashes = []
    no_of_frames = 1
    result_folder_path = './results'

    create_folder_for_video(result_folder_path)

    image_proc = multiprocessing.Process(target=extract_and_save_keyframes, args=[
                                         path_to_video, no_of_frames, result_folder_path])
    audio_proc = multiprocessing.Process(
        target=extract_and_save_audio, args=[path_to_video])

    image_proc.start()
    # audio_proc.start()

    image_proc.join()
    # audio_proc.join()

    for i in range(no_of_frames):
        feature_hashes.append(hash_image(
            result_folder_path + "/image"+str(i+1)+".png"))

    feature_hashes.append(hash_audio(result_folder_path+"/audio.mp3"))

    # remove_folder_for_video(result_folder_path)

    return feature_hashes


def compute_video_hash(path_to_video):
    feature_hash = get_feature_hash_from_video(path_to_video)
    return xor_elements(feature_hash)
    
def extract_one_frame(fileName):
    try:
        vidcap = cv2.VideoCapture(INPUT_FOLDER + fileName)
        # frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        # print('duration : ', duration, 'frame count: ', frame_count)
        
        vidcap.set(cv2.CAP_PROP_POS_MSEC, 2000)
        success, image = vidcap.read()
        if success:
            cv2.imwrite(OUTPUT_FOLDER+fileName+".png", image)
        else:
            print('did not extract frame correctly')
    except Exception as e:
        print('error extracting and saving keyframe ', e)

def get_video_hash_from_local_file(fileName):
    try:
        image_proc = multiprocessing.Process(target=extract_one_frame, args=[fileName])
        image_proc.start()
        image_proc.join()
        hash = hash_image(OUTPUT_FOLDER + fileName+".png")
        os.remove(OUTPUT_FOLDER + fileName + ".png")
        os.remove(INPUT_FOLDER + fileName)
        return hash, True
    except Exception as e:
        print('Error getting hash from local file ', e)
        return '', False

def get_video_hash_from_s3_file(fileName, bucketName, filePathPrefix):
    print('downloading ', fileName, 'from ', bucketName)
    try:
        with open(INPUT_FOLDER+fileName, 'wb') as f:
            s3.download_fileobj(bucketName, filePathPrefix + fileName, f)
        return get_video_hash_from_local_file(fileName)
    except Exception as e:
        print('error getting hash from s3 ', e)

def get_image_hash_from_local_file(fileName):
    try:
        hash = hash_image(INPUT_FOLDER + fileName)
        os.remove(INPUT_FOLDER + fileName)
        return hash, True
    except Exception as e:
        print('error getting image hash ', e)
        return '', False
        
def get_image_hash_from_s3_file(fileName, bucketName, filePathPrefix):
    print('downloading ', fileName, 'from ', bucketName)
    try:
        with open(INPUT_FOLDER+fileName, 'wb') as f:
            s3.download_fileobj(bucketName, filePathPrefix + fileName, f)
        return get_image_hash_from_local_file(fileName)
    except Exception as e:
        print('error getting hash from s3 file ', e)
        
def get_audio_hash_from_local_file(fileName):
    try:
        hash = hash_audio(INPUT_FOLDER + fileName)
        os.remove(INPUT_FOLDER + fileName)
        return hash, True
    except Exception as e:
        print('error getting image hash ', e)
        return '', False

def get_audio_hash_from_s3_file(fileName, bucketName, filePathPrefix):
    print('downloading ', fileName, 'from ', bucketName)

    def download_progress(byte_count):
        print('downloaded ', byte_count)

    try:
        with open(INPUT_FOLDER+fileName, 'wb') as f:
            s3.download_fileobj(bucketName, filePathPrefix + fileName, f, Callback=download_progress)
        return get_audio_hash_from_local_file(fileName)
    except Exception as e:
        print('error getting hash from s3 file ', e)