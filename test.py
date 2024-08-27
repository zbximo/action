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
import threading
import time
import argparse
import requests
import yaml

f = open('config.yaml', 'r')
config_data = yaml.load(f, Loader=yaml.FullLoader)
host_other = config_data['base_data']['other']['inflect']['ip'] + ":" + config_data['base_data']['other']['inflect'][
    'port']
host_teacher = config_data['base_data']['teacher']['inflect']['ip'] + ":" + \
               config_data['base_data']['teacher']['inflect'][
                   'port']
host_student = config_data['base_data']['student']['inflect']['ip'] + ":" + \
               config_data['base_data']['student']['inflect'][
                   'port']



def ifias():
    endpoint = r"/ifias"
    url = ''.join(["http://", host_other, endpoint])
    body = {
        "ts": {  # 这个ts用来返回analyze
            "teacher": [{
                "state": "stand",
                "writing": "speaking",

            }, {
                "state": "sit",
                "writing": "writing",

            }],
            "student": [0.6, 0.7, 0.8],
            # "vivid": False,# 这个由上面提供
            "walk": False,
        },
        "id": "44070",
        "course_id": "4624",
        "sub_id": "1011969",
        "trans_content": [
            {
                "BeginSec": 5,
                "Text": "好了。",
                "TransText": "All right.",
                "EndSec": 20
            },
            {
                "BeginSec": 20,
                "Text": "那个。",
                "TransText": "That.",
                "EndSec": 39
            },
            {
                "BeginSec": 39,
                "Text": "哦。",
                "TransText": "Oh.",
                "EndSec": 59
            },
            {
                "BeginSec": 59,
                "Text": "你说另外一种。",
                "TransText": "You said another.",
                "EndSec": 77
            },
            {
                "BeginSec": 77,
                "Text": "下面。",
                "TransText": "Below.",
                "EndSec": 96
            },
            {
                "BeginSec": 96,
                "Text": "啊。",
                "TransText": "Ah.",
                "EndSec": 210
            },
            {
                "BeginSec": 210,
                "Text": "别奇怪。",
                "TransText": "Don't be weird.",
                "EndSec": 233
            },
            {
                "BeginSec": 233,
                "Text": "不是还可以，就是买没那个啥，等于说是我们班那个。",
                "TransText": "Either it's okay, or if you don't have that one, it's the one in our class.",
                "EndSec": 271
            },
            {
                "BeginSec": 271,
                "Text": "对呀，在对。",
                "TransText": "Yes, yes.",
                "EndSec": 326
            },
            {
                "BeginSec": 326,
                "Text": "对呀，在对。",
                "TransText": "Yes, yes.",
                "EndSec": 600
            },
            {
                "BeginSec": 600,
                "Text": "对呀，在对。",
                "TransText": "Yes, yes.",
                "EndSec": 326
            },
            {
                "BeginSec": 600,
                "Text": "对呀，在对。请同学讲",
                "TransText": "Yes, yes.",
                "EndSec": 326
            }]}
    print(url)
    print(time.time())
    r = requests.post(url, data=json.dumps(body))
    print(time.time())
    print(json.loads(r.content))


def student():
    endpoint = r"/predict/student"
    url = ''.join(["http://", host_student, endpoint])
    body = {
        # 'img_url':'https://ximo-1306450197.cos.ap-shanghai.myqcloud.com/markdown/1EBA2718168B2FE7CAE2C6B93A56EF80.jpg'
        # 'img_url': 'https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/823103a9c5014dfab429b7f381234733~tplv-k3u1fbpfcp-watermark.image?'
        # 'img_url': 'http://10.61.254.250:8087/img/2022/09/15/15094_91427_14_42_1_1_4_3-4_J09003_20220915094150A373.jpg'
        # 教室没学生
        #'img_url': 'http://10.61.254.250:8087/img/2022/10/19/a4554fd3-25f5-4f0b-8676-57abeaae26ca_20221019141808A147.jpg'
        # 'img_url': 'http://10.66.10.234:8002/static/9548_31703_5_5_29_7_4_3,4_C10586.jpg'
        #'img_url': "http://10.61.254.250:8087/img/2022/11/11/b5a0afa4-90e8-4f6a-bfe8-6f7218929f1b_20221111151713A372.jpg"
	#'img_url': 'http://10.61.254.250:9000/uploadPath/2022/11/22/79392607-17c0-4c18-a5ab-9697355df381_20221122093517A995.jpg'
	#'img_url': 'http://10.61.254.250:8087/img/2023/02/27/92a8a2b9-e77b-429a-91d8-4996dde3e8d9_20230227154421A306.jpg'
	'img_url': 'https://patrol.hzcu.edu.cn/img/2024/04/24/e72b4668-98fd-4aea-b10e-81165cae4679_20240424090317A052.jpg'
	#'img_url':'http://10.61.254.250:8087/img/2022/09/28/19221_70351_14_42_1_3_3_1-2_C22018_20220928075537A155.jpg'
        # 404
        # 'img_url': 'http://10.61.254.250:8087/img/2022/09/28/19296_88297_14_42_1_3_3_3-4_C13520_20220928094529A720.jpg'
    }
    r = requests.post(url, data=body)
    print(r)
    print(json.loads(r.content))
    print(1, threading.current_thread())
    print(2, time.time())


def teacher():
    endpoint = r"/predict/teacher"
    url = ''.join(["http://", host_teacher, endpoint])
    body = {
        # 'img_url':'https://ximo-1306450197.cos.ap-shanghai.myqcloud.com/markdown/1EBA2718168B2FE7CAE2C6B93A56EF80.jpg'
        # 'img_url': 'https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/823103a9c5014dfab429b7f381234733~tplv-k3u1fbpfcp-watermark.image?'
         #'img_url': 'http://10.61.254.250:8087/img/2022/09/15/15094_91427_14_42_1_1_4_3-4_J09003_20220915094150A373.jpg'
        #'img_url': 'http://10.61.254.250:9000/uploadPath/2022/11/22/79392607-17c0-4c18-a5ab-9697355df381_20221122093517A995.jpg'
	'img_url': 'https://patrol.hzcu.edu.cn/img/2024/04/24/d8fe2b1b-62f9-41f2-a416-fe3167b26955_20240424083600A759.jpg'
	# 'img_url': 'http://10.66.10.234:8002/static/9548_31703_5_5_29_7_4_3,4_C10586.jpg'
        # 404
        # 'img_url': 'http://10.61.254.250:8087/img/2022/09/28/19221_70351_14_42_1_3_3_1-2_C22018_20220928075537A155.jpg'
        # blur
        #'img_url': "http://10.66.10.234:5011/static/blur_img/c15ccfa7-aba3-498a-9111-4f66194fd022_20221030151911A189.jpg"
    }
    r = requests.post(url, data=body)
    print(r)
    print(json.loads(r.content))
    print(1, threading.current_thread())
    print(2, time.time())


def walk():
    endpoint = r"/walk"
    url = ''.join(["http://", host_other, endpoint])
    body = {
        'shoulder_seq': json.dumps([-111, 111]),
        'max_space': 7
    }
    r = requests.post(url, data=body)
    print(r)
    print(json.loads(r.content))


def video():
    endpoint = r"/video"
    url = ''.join(["http://", host_other, endpoint])
    body = {
        'video_url': "http://10.61.254.250:9000/record/record/live/test/2022-10-21/13-37-46.mp4"
    }
    r = requests.post(url, data=body)
    print(r)
    print(json.loads(r.content))


# def test_student():
#     import time
#     def job1():
#         endpoint = r"/predict/student"
#         url = ''.join([host, endpoint])
#         body = {
#             # 'img_url':'https://ximo-1306450197.cos.ap-shanghai.myqcloud.com/markdown/1EBA2718168B2FE7CAE2C6B93A56EF80.jpg'
#             # 'img_url': 'https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/823103a9c5014dfab429b7f381234733~tplv-k3u1fbpfcp-watermark.image?'
#             'img_url': 'http://10.61.254.250:8087/img/2022/09/15/15094_91427_14_42_1_1_4_3-4_J09003_20220915094150A373.jpg'
#             # 'img_url': 'http://10.66.10.234:8002/static/9548_31703_5_5_29_7_4_3,4_C10586.jpg'
#             # 'img_url':'http://10.61.254.250:8087/img/2022/09/28/19221_70351_14_42_1_3_3_1-2_C22018_20220928075537A155.jpg'
#             # 404
#             # 'img_url': 'http://10.61.254.250:8087/img/2022/09/28/19296_88297_14_42_1_3_3_3-4_C13520_20220928094529A720.jpg'
#         }
#         r = requests.post(url, data=body)
#         print(r)
#         print(json.loads(r.content))
#         print(1, threading.current_thread())
#         print(2, time.time())
#
#     def job():
#         endpoint = r"/predict/teacher"
#         url = ''.join([host, endpoint])
#         body = {
#             # 'img_url':'https://ximo-1306450197.cos.ap-shanghai.myqcloud.com/markdown/1EBA2718168B2FE7CAE2C6B93A56EF80.jpg'
#             # 'img_url': 'https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/823103a9c5014dfab429b7f381234733~tplv-k3u1fbpfcp-watermark.image?'
#             'img_url': 'http://10.61.254.250:8087/img/2022/09/15/15094_91427_14_42_1_1_4_3-4_J09003_20220915094150A373.jpg'
#             # 'img_url': 'http://10.66.10.234:8002/static/9548_31703_5_5_29_7_4_3,4_C10586.jpg'
#             # 'img_url': 'http://10.61.254.250:8087/img/2022/09/28/19221_70351_14_42_1_3_3_1-2_C22018_20220928075537A155.jpg'
#         }
#         r = requests.post(url, data=body)
#         print(r)
#         print(json.loads(r.content))
#         print(1, threading.current_thread())
#         print(2, time.time())


def main():
    parser = argparse.ArgumentParser(description="Test")
    parser.add_argument('-n', '--name', default='student')
    parser.add_argument('-cnt', '--count', default=1)
    args = parser.parse_args()
    name = args.name
    count = int(args.count)
    if name == 'student':
        for i in range(0, count):
            t1 = threading.Thread(target=student, name="student: " + str(i))
            t1.start()
    elif name == 'teacher':
        for i in range(0, count):
            t1 = threading.Thread(target=teacher, name="teacher: " + str(i))
            t1.start()
    elif name == 'both':
        for i in range(0, count):
            t1 = threading.Thread(target=student, name="student: " + str(i))
            t1.start()
            t1 = threading.Thread(target=teacher, name="teacher: " + str(i))
            t1.start()
    elif name == 'ifias':
        for i in range(0, count):
            t1 = threading.Thread(target=ifias, name="ifias: " + str(i))
            t1.start()
    elif name == 'walk':
        for i in range(0, count):
            t1 = threading.Thread(target=walk, name="walk: " + str(i))
            t1.start()
    elif name == 'vedio':
        for i in range(0, count):
            t1 = threading.Thread(target=video, name="video: " + str(i))
            t1.start()


if __name__ == '__main__':
    main()
