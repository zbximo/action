# -*- encoding: utf-8 -*-
# @ModuleName: run_other
# @Function :
# @Author : ximo
# @Time : 2022/10/19 14:09

import json
import os
import threading
import time

from flask import Flask, request, make_response, jsonify
import numpy as np
from flask_cors import CORS
# import librosa
# from moviepy.video.io.VideoFileClip import VideoFileClip

from language import get_info
from datetime import date, timedelta

from util import remove_wav



app = Flask(__name__)
app.send_file_max_age_default = timedelta(seconds=1)
CORS(app)


@app.route('/ifias', methods=['POST'])
def get_ifias():
    data = request.get_data()
    # return jsonify(json.loads(data))

    data = json.loads(data)
    result = get_info(data)
    return jsonify({
        'code': 200,
        'data': result
    })


@app.route('/walk', methods=['POST'])
def get_walk():
    shoulder_seq = json.loads(request.form['shoulder_seq'])
    max_space = int(request.form['max_space'])
    shoulder_seq = [i for i in shoulder_seq if i is not None]
    ll = len(shoulder_seq)
    if max_space is None or ll == 0:
        result = False
    else:
        cnt = 0
        for i in range(len(shoulder_seq) - 1):
            if np.abs(shoulder_seq[i + 1] - shoulder_seq[i]) >= 2 * max_space:
                cnt += 1

        result = False if (cnt / ll <= 0.25) else True

    return jsonify({
        'code': 200,
        'data': {
            'walk': result
        }
    })


# @app.route('/video', methods=['POST'])
# def video():
#     try:
#         video_url = request.form['video_url']
#         video = VideoFileClip(video_url)
#         temp_path = 'temp/' + str(time.time()).replace('.', '-') + '.wav'
#         audio = video.audio
#         audio.write_audiofile(temp_path)
#         audio, freq = librosa.load(temp_path)
#         threading.Thread(remove_wav(temp_path)).start()
#         audio = librosa.to_mono(audio)
#     except:
#         return jsonify({
#             'code': 500,
#             'msg': 'error',
#             'data': {
#                 'video': 'video error'
#             }
#         })
#     if np.max(np.abs(audio)) < 5e-2:
#         return jsonify({
#             'code': 200,
#             'msg': 'success',
#             'data': {
#                 'video': 'small'
#             }
#         })
#     return jsonify({
#         'code': 200,
#         'msg': 'success',
#         'data': {
#             'video': 'normal'
#         }
#     })


if __name__ == '__main__':
    app.run()
