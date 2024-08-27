4# -*- encoding: utf-8 -*-
# @ModuleName: run_student
# @Function :
# @Author : ximo
# @Time : 2022/10/19 14:05
import json
import os
import threading
import yaml
import cv2
import requests
from flask import Flask, request, make_response, jsonify
import numpy as np
import mmcv
import glob

from flask_cors import CORS
from opera.apis import init_detector
from opera.infence import find_teacher, point
import base64
import torch
from language import get_info
from datetime import date, timedelta

from util import judge_blur_img, is404, create_dic

from log_req import log_with_name
app = Flask(__name__)
app.send_file_max_age_default = timedelta(seconds=1)
CORS(app)
config_file = 'opera/configs/inspose/inspose_r50_8x4_3x_coco.py'
checkpoint_file = 'opera/configs/inspose/inspose_r50_8x4_36e_coco.pth'
model_student = init_detector(config_file, checkpoint_file, device='cuda:1')
logger = log_with_name("student")
logger.info("student service restart")


@app.route('/predict/student', methods=['POST'])
def get_point():
    # threading.Thread(target=cuda_cache).start()
    # path = 'img/9483_5074_10_8_48_7_4_1,2_J02012.jpg'
    # img = mmcv.imread(path)
    # COS
    # print(111)
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400',
        "Content-Type": "application/jpeg"
    }

    img_url = request.form['img_url']
    logger.info("img_url: {}".format(str(img_url)))

    response = requests.get(url=img_url, headers=headers)
    logger.info("get img! url:{}".format(str(img_url)))    
    img = response.content
    # print(img,img_url)
    # # 本地图片
    # img = request.files['img']
    # img = img.read()
    try:
        img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
    except:
        res = {
            'code': 500,
            'data': {
                'error': "image error",
            }
        }
        del img
        return jsonify(res)
    if img is None:
        res = {
            'code': 500,
            'data': {
                'error': "image error",
            }
        }
        del img
        return jsonify(res)
    index = judge_blur_img(img)
    # print(222)
    if is404(img_np=img) or index >= 0.3:
        res = {
            'code': 500,
            'data': {
                'error': "image is 404 or so blur",
            }
        }
        del img
        return jsonify(res)
    else:

        file_name = 2
        # infence
        # num, [img, path], [imgwith, path_with], stu
        # result = point(model_student, img[150:, :, :], file_name)
        result = point(model_student, img, file_name)
        # return jsonify({
        #     "a":result
        # })
        if result is None:
            if index >= 0.15:
                res = {
                    'code': 200,
                    'data': {
                        'warning': "image is blur",
                    }
                }
                del img
                return jsonify(res)
            else:
                num = 0
                lookup = 0
                pos = '未知'
                img = np.ones((img.shape[0], img.shape[1], 3), dtype=np.uint8)
                img *= 255
        else:
            num = result[0]
            lookup = int(sum(np.array(result[-2])[:, -1]))

            pos = result[-1]
            img = result[1][0]
        # result = [num, path]
        # print(num, lookup)

        ll = img_url.split('/')
        img_name = ll[-1]
        f = open('config.yaml', 'r')
        config_data = yaml.load(f, Loader=yaml.FullLoader)
        host = config_data['base_data']['student']['inflect']['ip'] + ":" + \
               config_data['base_data']['student']['inflect'][
                   'port']
        # host = 'http://10.160.195.50:50'
        # host = 'http://173.0.85.5:5000'
        dic_path = create_dic('student')
        mmcv.imwrite(img, os.path.join(dic_path, img_name))
        # torch.cuda.empty_cache()
        res = {
            'code': 200,
            'data': {
                'num': num,
                'lookup': lookup,
                'img_url': os.path.join("http://", host, dic_path, img_name),
                'seat': pos
            }
        }
        del img
        logger.info("ret, url:{}".format(str(img_url)))    

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


if __name__ == '__main__':
    app.run()
