# -*- encoding: utf-8 -*-
# @ModuleName: test
# @Function :
# @Author : ximo
# @Time : 2022/6/26 22:54
import json
import os
import threading

import cv2
import requests
from flask import Flask, request, make_response, jsonify
import numpy as np
import mmcv
import glob
from opera.apis import init_detector
from opera.infence import find_teacher, point
import base64
import torch
from language import get_info
from datetime import date, timedelta

app = Flask(__name__)
app.send_file_max_age_default = timedelta(seconds=1)

# model = None
# checkpoint_file = 'opera/configs/inspose/inspose_r50_8x4_36e_coco.pth'
# global model
# def init_model():
#     config_file = 'opera/configs/inspose/inspose_r50_8x4_3x_coco.py'
#     checkpoint_file = 'opera/configs/inspose/inspose_r50_8x4_36e_coco.pth'
#     global model
#     model = init_detector(config_file, checkpoint_file, device='cuda:0')
config_file = 'opera/configs/inspose/inspose_r50_8x4_3x_coco.py'
checkpoint_file = 'opera/configs/inspose/inspose_r50_8x4_36e_coco.pth'
model_teacher = init_detector(config_file, checkpoint_file, device='cuda:0')
model_student = init_detector(config_file, checkpoint_file, device='cuda:1')


@app.route('/predict/te', methods=['POST', 'GET'])
def te():
    data = {
        'success': 'true',
        'code': 200
    }
    return jsonify(data)


@app.route('/predict/ttt', methods=['POST'])
def ttt():
    path = 'img/9454_32871_5_5_29_7_4_1,2_J05014.jpg'
    image_np = mmcv.imread(path)
    # # name file
    # img_str = request.form['image']
    # print(len(img_str))
    # if img_str is None:
    #     return 'no image file'
    # # 变成Numpy
    #
    # image_bytes = base64.b64decode(img_str)
    # image_np = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    print(image_np.shape)
    file_name = 2
    # infence
    r = point(model, image_np, file_name)
    result, img, imgwith = r[0], r[1][0], r[2][0]
    # result, img, imgwith = point(model, image_np, file_name)
    success, encoded_image = cv2.imencode(".png", img)
    image_bytes = encoded_image.tobytes()
    image_base64 = base64.b64encode(image_bytes).decode('utf8')
    print(len(image_base64))
    data = {
        'code': 200,
        'success': 'true',
        'data': {
            'image': image_base64,
        }

    }
    return jsonify(image_base64)


def is404(img_np):
    img = cv2.imread('static/404.jpg')
    if img.shape[0] != img_np.shape[0] or img.shape[1] != img_np.shape[1]:
        return False
    if (img == img_np).all():
        return True
    else:
        return False


def create_dic():
    time = date.today()
    dic_path = 'static/student_point/' + str(time.year) + '/' + str(time.month) + '/' + str(time.day)
    if not os.path.exists(dic_path):
        os.makedirs(dic_path)
    return dic_path


def cuda_cache():
    torch.cuda.empty_cache()


@app.route('/predict/student', methods=['POST'])
def get_point():
    threading.Thread(target=cuda_cache).start()
    # path = 'img/9483_5074_10_8_48_7_4_1,2_J02012.jpg'
    # img = mmcv.imread(path)
    # COS
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400',
        "Content-Type": "application/jpeg"
    }
    
    img_url = request.form['img_url']
    res = requests.get(url=img_url, headers=headers)
    img = res.content
    # # 本地图片
    # img = request.files['img']
    # img = img.read()
    try:
        img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
    except:
        res = {
            'code': 500,
            'data': {
                'error': "image url error",
            }
        }
        return jsonify(res)
    if img is None:
        res = {
            'code': 500,
            'data': {
                'error': "image url file",
            }
        }
        return jsonify(res)
    if is404(img_np=img):
        res = {
            'code': 500,
            'data': {
                'error': "image is 404",
            }
        }
        return jsonify(res)
    file_name = 2
    # infence
    # num, [img, path], [imgwith, path_with], stu
    result = point(model_student, img, file_name)

    img = result[1][0]
    ll = img_url.split('/')
    img_name = ll[-1]
    host = 'http://173.0.85.5:5000'
    dic_path = create_dic()
    mmcv.imwrite(img, os.path.join(dic_path, img_name))
    if result is None:
        num = 0
        lookup = 0
        pos = '未知'
    else:
        num = result[0]
        lookup = int(np.sum(result[-2][-1] is False))
        pos = result[-1]
    # result = [num, path]
    print(num, lookup)
    # torch.cuda.empty_cache()
    res = {
        'code': 200,
        'data': {
            'num': num,
            'lookup': lookup,
            'img_url': os.path.join(host, dic_path, img_name),
            'seat': pos
        }
    }

    return jsonify(res)
    # if num is None or num == 0:
    #     print('no student')
    #     res = {
    #         'code': 200,
    #         'data': {
    #             'num': 'false',
    #         }
    #     }
    #     return res
    # else:
    #     res = {
    #         'code': 200,
    #         'data': {
    #             'exist': 'false',
    #         }
    #     }
    #     return res
    # path = '/home/amax/haidongxu/python/point/' + str(3) + '.png'
    # mmcv.imwrite(img, path)
    # path = '/home/amax/haidongxu/python/point/' + str(3) + '1.png'
    # mmcv.imwrite(imgwith, path)
    # success, encoded_image = cv2.imencode(".png", img)
    # print(sorted(stu, key=lambda x: x[0]))
    # img_stream = encoded_image.tostring()
    # response = make_response(img_stream)
    # response.headers['Content-Type'] = 'image/png'


@app.route('/predict/teacher', methods=['POST'])
def get_teacher():
    threading.Thread(target=cuda_cache).start()
    # # test
    # path = 'img/18832_643_6_1_2_11_4_1,2_C21025.jpg'
    # img = mmcv.imread(path)
    # # COS
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400',
        "Content-Type": "application/jpeg"
    }
    img_url = request.form['img_url']
    response = requests.get(url=img_url, headers=headers)
    img = response.content
    # # 本地图片
    # img = request.files['img']
    # if img is None:
    #     return 'no image file'
    # img = img.read()
    try:
        img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
    except:
        res = {
            'code': 500,
            'data': {
                'error': "image url error",
            }
        }
        return jsonify(res)
    if img is None:
        res = {
            'code': 500,
            'data': {
                'error': "image url error",
            }
        }
        return jsonify(res)
    if is404(img_np=img):
        res = {
            'code': 500,
            'data': {
                'error': "image is 404",
            }
        }
        return jsonify(res)
    # infence
    result = find_teacher(model_teacher, img)
    # result = [state, direction, writing]
    # [stand or sit, side or back or front, writing or speaking]

    if result is None:
        print('no teacher')
        res = {
            'code': 200,
            'data': {
                'exist': 'false',
            }
        }
        return jsonify(res)
    else:
        print(result)
        res = {
            'code': 200,
            'data': {
                'exist': 'true',
                'state': result[0],
                'direction': result[1],
                "writing": result[2],
                'left_shoulder': int(result[3]),
                'right_shoulder': int(result[4])
            }
        }
        return jsonify(res)


@app.route('/ifias', methods=['POST'])
def get_ifias():
    docx_url = request.form['docx_url']
    result = get_info(docx_url)
    return jsonify({
        'code': 200,
        'data': result
    })


@app.route('/walk', methods=['POST'])
def get_walk():
    shoulder_seq = json.loads(request.form['shoulder_seq'])
    max_space = int(request.form['max_space'])
    ll = len(shoulder_seq)
    cnt = 0
    for i in range(len(shoulder_seq) - 1):
        if np.abs(shoulder_seq[i + 1] - shoulder_seq[i]) >= 2 * max_space:
            cnt += 1

    result = True if cnt / ll > 0.25 else False

    return jsonify({
        'code': 200,
        'data': {
            'walk': result
        }
    })


if __name__ == '__main__':
    # init_model()
    app.run('173.0.85.5',debug=True, threaded=True)
