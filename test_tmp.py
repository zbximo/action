# # -*- encoding: utf-8 -*-
# # @ModuleName: test
# # @Function :
# # @Author : ximo
# # @Time : 2022/7/5 10:26
# # -*- coding: utf-8 -*-
# import mmcv
# import requests
# import json
# import time
# import base64
#
import json
import multiprocessing
import re
import threading
import time
from datetime import date

import torch.cuda

host = "http://173.0.85.5:5000"

# headers = \
#     {
#         "applicationCode": "detection",
#         "operationTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
#         "Content-Type": "application/json;charset=UTF-8"
#     }
# path = 'https://ximo-1306450197.cos.ap-shanghai.myqcloud.com/markdown/1EBA2718168B2FE7CAE2C6B93A56EF80.jpg'
#
# img = mmcv.imread(path)
# imgbase64 = base64.b64encode(img)
# body = \
#     {
#         "img": imgbase64
#     }
# r = requests.post(url, headers=headers, data=body)
import requests


# headers = \
#     {
#         "Content-Type": "application/form-data"
#     }
# # x = requests.get(url='https://ximo-1306450197.cos.ap-shanghai.myqcloud.com/markdown/1EBA2718168B2FE7CAE2C6B93A56EF80.jpg')
# # print(x.content)


def teacher_student():
    def job():
        endpoint = r"/predict/teacher"
        url = ''.join([host, endpoint])
        body = {
            # 'img_url':'https://ximo-1306450197.cos.ap-shanghai.myqcloud.com/markdown/1EBA2718168B2FE7CAE2C6B93A56EF80.jpg'
            'img_url': 'https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/823103a9c5014dfab429b7f381234733~tplv-k3u1fbpfcp-watermark.image?'
        }
        r = requests.post(url, data=body)
        print(json.loads(r.content))
        print(threading.current_thread())
        print(time.time())

    print(time.time())
    for i in range(0, 1):
        t1 = threading.Thread(target=job, name=str(i))
        t1.start()
    # r = requests.get('https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/823103a9c5014dfab429b7f381234733~tplv-k3u1fbpfcp-watermark.image?')
    # print(r.content)


def test_ifias():
    endpoint = r"/ifias"
    url = ''.join([host, endpoint])
    body = {
        # 'docx_url': 'https://source.cmc.zucc.edu.cn/uploads/2022/Aug/20220820131928t1hvoh5d430e.docx'
        'docx_url': 'https://source.cmc.zucc.edu.cn/uploads/2022/Sep/20220920151626hthysfi9yk3y.docx'
    }
    print(url)
    print(time.time())
    r = requests.post(url, data=body)
    print(time.time())
    print(r.content)
    try:
        print(json.loads(r.content))
    except:
        print(endpoint)


def test_student():
    import time
    def job1():
        endpoint = r"/predict/student"
        url = ''.join([host, endpoint])
        body = {
            # 'img_url':'https://ximo-1306450197.cos.ap-shanghai.myqcloud.com/markdown/1EBA2718168B2FE7CAE2C6B93A56EF80.jpg'
            # 'img_url': 'https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/823103a9c5014dfab429b7f381234733~tplv-k3u1fbpfcp-watermark.image?'
             'img_url': 'http://10.61.254.250:8087/img/2022/09/15/15094_91427_14_42_1_1_4_3-4_J09003_20220915094150A373.jpg'
            # 'img_url': 'http://10.66.10.234:8002/static/9548_31703_5_5_29_7_4_3,4_C10586.jpg'
            #'img_url':'http://10.61.254.250:8087/img/2022/09/28/19221_70351_14_42_1_3_3_1-2_C22018_20220928075537A155.jpg'
            # 404
            # 'img_url': 'http://10.61.254.250:8087/img/2022/09/28/19296_88297_14_42_1_3_3_3-4_C13520_20220928094529A720.jpg'
        }
        r = requests.post(url, data=body)
        print(r)
        print(json.loads(r.content))
        print(1, threading.current_thread())
        print(2, time.time())

    def job():
        endpoint = r"/predict/teacher"
        url = ''.join([host, endpoint])
        body = {
            # 'img_url':'https://ximo-1306450197.cos.ap-shanghai.myqcloud.com/markdown/1EBA2718168B2FE7CAE2C6B93A56EF80.jpg'
            # 'img_url': 'https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/823103a9c5014dfab429b7f381234733~tplv-k3u1fbpfcp-watermark.image?'
             'img_url': 'http://10.61.254.250:8087/img/2022/09/15/15094_91427_14_42_1_1_4_3-4_J09003_20220915094150A373.jpg'
            #'img_url': 'http://10.66.10.234:8002/static/9548_31703_5_5_29_7_4_3,4_C10586.jpg'
            # 'img_url': 'http://10.61.254.250:8087/img/2022/09/28/19221_70351_14_42_1_3_3_1-2_C22018_20220928075537A155.jpg'
        }
        r = requests.post(url, data=body)
        print(r)
        print(json.loads(r.content))
        print(1, threading.current_thread())
        print(2, time.time())

    for i in range(0, 1):
        t1 = threading.Thread(target=job, name=str(000) + str(i))
        t1.start()
        t1 = threading.Thread(target=job1, name=str(111))
        t1.start()

    print(5, time.time())


def test_walk():
    import time
    def job():
        endpoint = r"/walk"
        url = ''.join([host, endpoint])
        body = {
            'shoulder_seq': json.dumps([-111, 111]),
            'max_space': 7
        }
        r = requests.post(url, data=body)
        print(r)
        print(json.loads(r.content))

    for i in range(0, 1):
        t1 = threading.Thread(target=job, name=str(i))
        t1.start()

    print(5, time.time())

test_student()
