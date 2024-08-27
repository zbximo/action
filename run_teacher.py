# -*- encoding: utf-8 -*-
# @ModuleName: run_teacher
# @Function :
# @Author : ximo
# @Time : 2022/10/19 14:04

import cv2
import requests
from flask import Flask, request, make_response, jsonify
import numpy as np
from opera.apis import init_detector
from opera.infence import find_teacher, point
from datetime import date, timedelta
# from flask_cors import CORS
from util import is404, judge_blur_img
from log_req import log_with_name

app = Flask(__name__)
app.send_file_max_age_default = timedelta(seconds=1)
# CORS(app)
config_file = 'opera/configs/petr/petr_r50_16x2_100e_coco.py'
checkpoint_file = 'opera/configs/petr/petr_r50_16x2_100e_coco.pth'
model_teacher = init_detector(config_file, checkpoint_file, device='cuda:0')
logger = log_with_name("teacher")

logger.info("teacher service restart")


@app.route('/predict/tt', methods=['POST'])
def t():
    return jsonify({
        'a': 'aaa'
    })


@app.route('/predict/teacher', methods=['POST'])
def get_teacher():
    # # test
    # path = 'img/18832_643_6_1_2_11_4_1,2_C21025.jpg'
    # img = mmcv.imread(path)
    # # COS
    # print(111)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400',
        "Content-Type": "application/jpeg"
    }
    img_url = request.form['img_url']
    logger.info("img_url: {}".format(str(img_url)))

    response = requests.get(url=img_url, headers=headers)
    logger.info("get img!  url:{}".format(str(img_url)))

    img = response.content
    # print(222)
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
    if is404(img_np=img) or index >= 0.5:
        res = {
            'code': 500,
            'data': {
                'error': "image is 404 or so blur",
            }
        }
        del img
        return jsonify(res)
    else:
        # infence
        # result = [state, direction, writing]
        # [stand or sit, side or back or front, writing or speaking]
        result = find_teacher(model_teacher, img)
        # print(333)
        if result is None:
            if index >= 0.15:
                res = {
                    'code': 200,
                    'data': {
                        'exist': 'false',
                        'warning': "image is blur",
                    }
                }
            else:
                res = {
                    'code': 200,
                    'data': {
                        'exist': 'false',
                    }
                }
            del img
            return jsonify(res)
        else:
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
            del img
            logger.info("ret, url:{}".format(str(img_url)))    

            return jsonify(res)
    # # infence
    # result = find_teacher(model_teacher, img)
    # # result = [state, direction, writing]
    # # [stand or sit, side or back or front, writing or speaking]
    #
    # if result is None:
    #     print('no teacher')
    #     res = {
    #         'code': 200,
    #         'data': {
    #             'exist': 'false',
    #         }
    #     }
    #     return jsonify(res)
    # else:
    #     print(result)
    #     res = {
    #         'code': 200,
    #         'data': {
    #             'exist': 'true',
    #             'state': result[0],
    #             'direction': result[1],
    #             "writing": result[2],
    #             'left_shoulder': int(result[3]),
    #             'right_shoulder': int(result[4])
    #         }
    #     }
    #     return jsonify(res)


if __name__ == '__main__':
    app.run()
