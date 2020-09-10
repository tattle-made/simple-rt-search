# importing required modules
from Katna.video import Video
import timeit
import pandas as pd
import matplotlib.pyplot as plt
import os
import moviepy.editor
from mp3hash import mp3hash
from PIL import Image
import imagehash
import timeit
import shutil
import multiprocessing


def create_folder_for_video(path):
    os.makedirs(path)


def get_key_frames_from_video(path_to_video, no_of_frames):
    video = Video()
    images = video.extract_frames_as_images(
        no_of_frames=no_of_frames, file_path=path_to_video)
    return images


def write_images_into_folder(images, no_of_frames, path):
    video = Video()
    for i in range(no_of_frames):
        video.save_frame_to_disk(
            images[i], file_path=path, file_name="image"+str(i+1), file_ext=".png")


def get_audio_from_video(path_to_video):
    video = moviepy.editor.VideoFileClip(path_to_video)
    return video.audio


def write_audio_into_folder(audio, path):
    audio.write_audiofile(path)


def extract_and_save_keyframes(path_to_video, no_of_frames, result_folder_path):
    key_frames = get_key_frames_from_video(path_to_video, no_of_frames)
    write_images_into_folder(key_frames, no_of_frames, result_folder_path)


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
    no_of_frames = 10
    result_folder_path = './results'

    create_folder_for_video(result_folder_path)

    image_proc = multiprocessing.Process(target=extract_and_save_keyframes, args=[
                                         path_to_video, no_of_frames, result_folder_path])
    audio_proc = multiprocessing.Process(
        target=extract_and_save_audio, args=[path_to_video])

    image_proc.start()
    audio_proc.start()

    image_proc.join()
    audio_proc.join()

    for i in range(no_of_frames):
        feature_hashes.append(hash_image(
            result_folder_path + "/image"+str(i+1)+".png"))

    feature_hashes.append(hash_audio(result_folder_path+"/audio.mp3"))

    remove_folder_for_video(result_folder_path)

    return feature_hashes


def compute_video_hash(path_to_video):
    feature_hash = get_feature_hash_from_video(path_to_video)
    return xor_elements(feature_hash)


image_proc = multiprocessing.Process(target=extract_and_save_keyframes, args=[
                                     "/Users/anushree/tattle/sample_videos/fruitseller.mp4", 15, './results'])
audio_proc = multiprocessing.Process(target=extract_and_save_audio, args=[
                                     "/Users/anushree/tattle/sample_videos/fruitseller.mp4"])


if __name__ == '__main__':
    video_hash = compute_video_hash(
        "/Users/anushree/tattle/sample_videos/fruitseller.mp4")
    print(video_hash)
