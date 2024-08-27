# -*- encoding: utf-8 -*-
# @ModuleName: run_viedo
# @Function :
# @Author : ximo
# @Time : 2022/10/20 14:43
import os
import random
import threading

import numpy as np
import time

import requests
from moviepy.editor import VideoFileClip
import librosa
import cv2

# import requests
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400',
#     "Content-Type": "application/jpeg"
# }
# video_url = 'http://10.61.254.250:9000/record/record/live/test/2022-10-20/11-14-17.mp4'
# res = requests.get(url=video_url, headers=headers)
# video = res.content
little_audio = [
    'http://10.61.254.250:9000/record/record/live/test2/2022-10-20/14-55-41.mp4',
    'http://10.61.254.250:9000/record/record/live/test3/2022-10-20/14-57-57.mp4'
]
no_audio = [
    'http://10.61.254.250:9000/record/record/live/test5/2022-10-20/15-28-32.mp4'
]
has_audio = [
    'http://10.61.254.250:9000/record/record/live/test/2022-10-20/11-14-17.mp4',
    'http://10.61.254.250:9000/record/record/live/test4/2022-10-20/15-25-13.mp4'
]


def plot(audio, freq):
    import matplotlib.pyplot as plt

    time = np.arange(0, len(audio)) / freq
    # np.arange(0, len(audio))  = (0,1,2,3,...,2079314)
    print(time.shape)  # (2079315,)
    print(np.min(time), np.max(time))  # 94.29995464852608  0.0
    print(np.mean(np.abs(audio)))
    fig, ax = plt.subplots()
    ax.plot(time, audio)
    ax.set(xlabel="Time(s)", ylabel="Sound Amplitude")
    plt.show()


def get_video_duration(filename):
    cap = cv2.VideoCapture(filename)
    _, frame = cap.read()
    print(frame)
    if cap.isOpened():
        rate = cap.get(5)
        frame_num = cap.get(7)
        duration = frame_num / rate
        print(duration)
        return duration
    return -1


def remove_wav(file_path):
    os.remove(file_path)


def run(video_url):
    video = VideoFileClip(video_url)
    time_video = video.duration
    print(time_video)
    print(list(np.arange(0, time_video, 0.5)))
    l = random.sample(list(np.arange(0, time_video, 0.5)), 2)
    for i in l:
        x = video.get_frame(i)
        print(x)
    # rand_time = np.random.randint()


def detect_audio(video_url):
    try:
        video = VideoFileClip(video_url)
        temp_path = 'temp/' + str(time.time()).replace('.', '-') + '.wav'
        audio = video.audio
        audio.write_audiofile(temp_path)
        audio, freq = librosa.load(temp_path)
        threading.Thread(remove_wav(temp_path)).start()
        audio = librosa.to_mono(audio)
    except:
        print('no')
        return False
    time_len = len(audio) / freq
    print(time_len)

    time_len = np.arange(0, len(audio)) / freq
    plot(audio, freq)
    # print(time_len.shape, freq)  # (2079315,)
    # print(np.min(time_len), np.max(time_len))  # 0.0   94.29995464852608
    print(np.mean(np.abs(audio)), np.min(audio), np.max(audio))
    if np.max(np.abs(audio)) < 5e-2:
        print('no')
        return False
    return True


if __name__ == '__main__':
    # for i in no_audio:
    #     print('*' * 10)
    #     detect_audio(i, 'temp/1.wav')
    # for i in has_audio:
    #     print('*' * 10)
    #     detect_audio(i, 'temp/1.wav')
    with open('视频地址.txt', 'r') as f:
        audios = f.readlines()
    print(audios)
    for i in audios:
        url, label = i.split(' ')[0], i.split(' ')[1]
        result = detect_audio(url)
        print(result, label)
        # get_video_duration(url)
        # break
