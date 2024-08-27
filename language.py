import copy
import json

import numpy as np
import math
import os.path
import re
import time
from html.parser import HTMLParser
from zipfile import ZipFile

import yaml
from cnsenti import Sentiment
from bixin import predict
import requests
import datetime

from plot_fig import plot_ifias, get_word_cloud


def isdocx(zf):
    if not zf.namelist().__contains__('word/document.xml'):
        # print('invalid MS word file.')
        return False
    return True


class Parser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = ''
        self.cnt = 0

    def handle_data(self, data):
        self.text += data

        self.cnt += 1

    def handle_endtag(self, tag):
        if tag == 'w:p' or tag == 'w:br':  # new line
            self.text += '\n'

            self.cnt += 1


def docx2txt(file_path):
    zf = ZipFile(file_path)
    r = isdocx(zf)
    if r is False:
        return "trans error"
    text = str(zf.read('word/document.xml'), encoding='utf-8')
    p = Parser()
    p.feed(text)
    p.close()
    text = p.text
    return text


def to_hms(second):
    m, s = divmod(second, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


def get_info(data):
    with open('./dictionary/teach.txt', encoding='utf-8') as f0:
        list_teach = eval(f0.read())
    with open('./dictionary/accept.txt', encoding='utf-8') as f1:
        list_accept = eval(f1.read())
    with open('./dictionary/close_q.txt', encoding='utf-8') as f2:
        list_close = eval(f2.read())
    with open('./dictionary/command.txt', encoding='utf-8') as f3:
        list_command = eval(f3.read())
    with open('./dictionary/praise.txt', encoding='utf-8') as f4:
        list_praise = eval(f4.read())
    with open('./dictionary/criticism.txt', encoding='utf-8') as f5:
        list_criticism = eval(f5.read())
    with open('./dictionary/adopt_student.txt', encoding='utf-8') as f6:
        list_adopt_student = eval(f6.read())
    # 学生回答次数
    with open('./dictionary/student_answer.txt', encoding='utf-8') as f7:
        list_student_answer = eval(f7.read())
    f0.close()
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()
    f6.close()
    f7.close()
    # file_path = './input/金融法规3.docx'
    senti = Sentiment()
    raw_result = []
    trans_data = data["trans_content"]
    # print(111,trans_data)

    # 抬头率
    atmosphere = "学生专注度偏低、学习氛围有待改进"  # 默认
    if (np.median(data['ts']["student"]) > 0.8):  # 判断抬头率返回文字
        atmosphere = "学生专注度高、学习氛围教好"
    # 教学风格

    for i in range(len(trans_data)):
        line = to_hms(trans_data[i]['BeginSec']) + '：' + trans_data[i]['Text']
        raw_result.append(line)
    # 得到'00:00:21：变造人民币。'的一个列表
    time_result = []
    result = []
    for i in range(len(raw_result)):
        if raw_result[i] == '':
            break
        time_result.append(datetime.datetime.strptime(raw_result[i][:8], '%H:%M:%S'))
        result.append(raw_result[i][9:])
    # print(111, result)
    list_behave = []
    time_result_zero = time_result.copy()
    # 找出时间节点
    time_start = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    for i in range(len(time_result)):
        if time_result[i] > time_start:
            if i != 0:
                time_result[i] = 0
            time_start += datetime.timedelta(minutes=5)

    # list_time_count = []
    # temp_count = 0
    # for m1 in time_result:
    #     temp_count += 1
    #     if m1 == 0:
    #         list_time_count.append(temp_count - 1)
    #         temp_count = 1

    def classify(s):
        r = [0]
        if '同学' in s and ('请' in s or '让' in s or '有没有' in s or '找'):
            for x in list_student_answer:
                if x in s:
                    r[0] = 1
                    break

        for x in list_accept:
            if x in s and s[s.find("觉得") - 1] != "我":
                # list_behave.append(1)
                r.append(1)
                return r
                # return 1

        for x in list_criticism:
            if x in s:
                # list_behave.append(8)
                # return 8
                r.append(8)
                return r
        for x in list_adopt_student:
            if x in s:
                # list_behave.append(3)
                # return 3
                r.append(3)
                return r
        if "？" in s:
            for i in list_close:
                if i in s:
                    # print("是封闭性问题")
                    # list_behave.append(5)
                    # return 5
                    r.append(5)
                    return r
            # print("是开放性问题")
            # list_behave.append(4)
            # return 4
            r.append(4)
            return r
        else:
            for y in list_command:
                if y in s:
                    # print("是指令")
                    # list_behave.append(7)
                    # return 7
                    r.append(7)
                    return r
            for x in list_praise:
                if x in s:
                    # list_behave.append(2)
                    # return 2
                    r.append(2)
                    return r
            # list_behave.append(6)
            # return 6
            r.append(6)
            return r

    def classify_emotion(s):
        # result = SnowNLP(s)
        result1 = senti.sentiment_calculate(s)
        result = predict(s)
        if result <= -0.5 and result1['neg'] > result1['pos'] and result1['neg'] > 1:
            # print(s)
            return 0
        else:
            return 1

    list_ts = [classify(i) for i in result]  # [[0,1],[1,10]] n * [学生回答，互动行为类别]
    list_student = np.array(list_ts)[:, 0].tolist()
    count_answer = list_student.count(1)
    list_type = np.array(list_ts)[:, 1].tolist()
    # 定义时间段
    time_s = datetime.datetime.strptime('00:00:30', '%H:%M:%S') - datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    time_e = datetime.datetime.strptime('00:00:38', '%H:%M:%S') - datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    time_d = datetime.datetime.strptime('00:00:15', '%H:%M:%S') - datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    # list_type = [classify(i) for i in result]
    # print(len(time_result),len(result))
    # print(result)
    list_behave.append(classify(result[0])[1])

    for t in range(1, len(time_result)):
        start = time_result_zero[t - 1]
        end = time_result_zero[t]
        if end - start > time_s and end - start < time_e:
            list_behave.append(13)
        elif end - start > time_e:
            cc = math.ceil((end - start).total_seconds() / time_d.total_seconds())
            list_behave.extend([13] * cc)
        list_behave.append(classify(result[t])[1])  # 每个句子进行识别并标注到列表
    # print(list_behave)  # 保留了沉寂
    # 判断课堂结构
    structure = "以教师教学为主"
    if list_behave.count(13) / len(list_behave) > 0.5:
        structure = "教师教学与学生练习相结合"
    list_behave_copy = [i for i in list_behave if i != 13]
    # print(list_behave_copy)  # 去掉了沉寂
    # list_behave_merge(把13压缩到一起)
    list_behave_merge = []
    silence = 0  # 记录沉寂数
    for x1 in list_behave:
        if x1 != 13:
            if silence == 0:
                list_behave_merge.append(x1)
            else:
                list_behave_merge[-1] = str(list_behave_merge[-1]) + "_" + str(silence)
                silence = 0  # 沉寂总次数
                list_behave_merge.append(x1)
        else:
            silence += 1
    # print(list_behave_merge)
    # print(list_behave)
    # 情感二分类
    # list_emotion = []
    pos_sum = 0
    neg_sum = 0
    # list_emotion = [classify_emotion(i) for i in result]
    # for i in result:
    #     list_emotion.append(classify_emotion(i))
    teach_count = 0
    accept = 0
    command = 0
    close_q = 0
    open_q = 0
    praise = 0
    criticism = 0
    adopt = 0
    for i in list_type:
        if i == 1:
            accept += 1
        elif i == 2:
            praise += 1
        elif i == 3:
            adopt += 1
        elif i == 4:
            open_q += 1
        elif i == 5:
            close_q += 1
        elif i == 6:
            teach_count += 1
        elif i == 7:
            command += 1
        else:
            criticism += 1
    # for i in list_emotion:
    #     if i == 1:
    #         pos_sum += 1
    #     else:
    #         neg_sum += 1
    sum_count = len(list_behave) - list_behave.count(13)
    # print(list_type)
    # print(teach_count / sum_count)
    # 插入时间片
    dict_list = []
    dict_id_name = {
        1: 'accept', 2: 'praise', 3: 'adopt', 4: 'open_question', 5: 'close_question', 6: 'teach_count', 7: 'command',
        8: 'criticism', 13: 'silence'
    }
    temp_dict = {'sum': 0, 'accept': 0, 'praise': 0, 'adopt': 0, 'open_question': 0, 'close_question': 0,
                 'teach_count': 0, 'command': 0, 'criticism': 0, 'silence': 0}
    # print(time_result)

    for m2 in range(len(time_result)):
        if m2 == len(time_result) - 1:
            temp_dict[dict_id_name[list_behave_copy[m2]]] += 1
            temp_dict['sum'] += 1
            dict_list.append(temp_dict)
        elif time_result[m2] == 0:
            dict_list.append(temp_dict)
            temp_dict = {'sum': 0, 'accept': 0, 'praise': 0, 'adopt': 0, 'open_question': 0, 'close_question': 0,
                         'teach_count': 0, 'command': 0, 'criticism': 0, 'silence': 0}
            if type(list_behave_merge[m2]) is str:  # 说明碰到沉寂
                temp_dict[dict_id_name[list_behave_copy[m2]]] += 1
                temp_dict["silence"] += int(list_behave_merge[m2].split('_')[1])
                temp_dict['sum'] += int(list_behave_merge[m2].split('_')[1]) + 1  # 因为不能忽略本身
            else:
                temp_dict[dict_id_name[list_behave_copy[m2]]] += 1
                temp_dict['sum'] += 1
        else:
            if type(list_behave_merge[m2]) is str:  # 说明碰到沉寂
                temp_dict[dict_id_name[list_behave_copy[m2]]] += 1
                temp_dict["silence"] += int(list_behave_merge[m2].split('_')[1])
                temp_dict['sum'] += int(list_behave_merge[m2].split('_')[1]) + 1
            else:
                temp_dict[dict_id_name[list_behave_copy[m2]]] += 1
                temp_dict['sum'] += 1

    # print(len(dict_list))
    f = open('config.yaml', 'r')
    config_data = yaml.load(f, Loader=yaml.FullLoader)
    host = config_data['base_data']['other']['inflect']['ip'] + ":" + config_data['base_data']['other']['inflect'][
        'port']
    #
    # # host = 'http://10.66.10.234:8002'
    # # print(len(list_behave), len(time_result), len(list_type), file_name)
    filename = ''.join([data['id'], data['course_id'], data['sub_id']])
    # print(list_behave)
    png_path, png_area_path = plot_ifias(list_behave, filename)
    word_cloud_path = get_word_cloud(result, filename)
    if word_cloud_path:
        word_cloud_url = os.path.join("http://", host, word_cloud_path)
    else:
        word_cloud_url = word_cloud_path
    if teach_count / len(list_type) > 0.65:  # 这里不考虑沉寂
        vivid = False
    else:
        vivid = True

    # 判断style
    def teachingStyle(data):
        teach_list = []  # stand,sit,write
        for i in data["teacher"]:
            teach_list.append(i['state'])
            teach_list.append(i['writing'])
        introduce = "老师"
        style = "属于"
        stand = teach_list.count('stand') / (teach_list.count('stand') + teach_list.count('sit'))
        writing = teach_list.count('writing') / len(teach_list)
        if (1 - stand) > 0.8:
            introduce += "教师大部分时间坐着,偶尔站着,"
        else:
            introduce += "教师大部分时间站着,偶尔坐着,"
        if writing > 5:
            introduce += "经常写板书，"
        else:
            introduce += "偶尔写板书,"
        if vivid:
            introduce += "上课积极性高,"
            style += '积极型、'
        if not data["walk"]:
            introduce += "长时间在一个位置不走动,"
            style += '执行型、'
        else:
            introduce += "经常有走动,"
            style += '激进型、'

        return {
            "teacher": {"stand": stand,
                        "sit": 1 - stand,
                        "style": introduce + style[:-1]},
            "student": {"uprate": np.median(data["student"])}
        }

    analyze_result = teachingStyle(data['ts'])
    analyze_result['atmosphere'] = atmosphere
    analyze_result['structure'] = structure

    return {
        'sum': sum_count,
        'student_answer': count_answer,
        'analyze': analyze_result,
        'ifias': {
            'img_url': os.path.join("http://", host, png_path),
            'img_area_url': os.path.join("http://", host, png_area_path),
            'word_cloud_url': word_cloud_url,
            'behave_time_count': dict_list
        }
    }


if __name__ == '__main__':
    print(time.time())
    # d = {
    #     "ts": {  # 这个ts用来返回analyze
    #         "teacher": [{
    #             "state": "stand",
    #             "writing": "speaking"
    #         }, {
    #             "state": "sit",
    #             "writing": "writing"
    #         }],
    #         "student": [0.6, 0.7, 0.8],
    #         # "vivid": False,# 这个由上面提供
    #         "walk": False,
    #     },
    #     "id": "44070",
    #     "course_id": "4624",
    #     "sub_id": "1011969",
    #     "trans_content": [
    #         {
    #             "BeginSec": 5,
    #             "Text": "好了。",
    #             "TransText": "All right.",
    #             "EndSec": 20
    #         },
    #         {
    #             "BeginSec": 20,
    #             "Text": "那个。",
    #             "TransText": "That.",
    #             "EndSec": 39
    #         },
    #         {
    #             "BeginSec": 39,
    #             "Text": "哦。",
    #             "TransText": "Oh.",
    #             "EndSec": 59
    #         },
    #         {
    #             "BeginSec": 59,
    #             "Text": "你说另外一种。",
    #             "TransText": "You said another.",
    #             "EndSec": 77
    #         },
    #         {
    #             "BeginSec": 77,
    #             "Text": "下面。",
    #             "TransText": "Below.",
    #             "EndSec": 96
    #         },
    #         {
    #             "BeginSec": 96,
    #             "Text": "啊。",
    #             "TransText": "Ah.",
    #             "EndSec": 210
    #         },
    #         {
    #             "BeginSec": 210,
    #             "Text": "别奇怪。",
    #             "TransText": "Don't be weird.",
    #             "EndSec": 233
    #         },
    #         {
    #             "BeginSec": 233,
    #             "Text": "不是还可以，就是买没那个啥，等于说是我们班那个。",
    #             "TransText": "Either it's okay, or if you don't have that one, it's the one in our class.",
    #             "EndSec": 271
    #         },
    #         {
    #             "BeginSec": 271,
    #             "Text": "对呀，在对。让同学",
    #             "TransText": "Yes, yes.",
    #             "EndSec": 326
    #         },
    #         {
    #             "BeginSec": 326,
    #             "Text": "对呀，在对。",
    #             "TransText": "Yes, yes.",
    #             "EndSec": 600
    #         },
    #         {
    #             "BeginSec": 600,
    #             "Text": "对呀，在对。请同学讲",
    #             "TransText": "Yes, yes.",
    #             "EndSec": 326
    #         }]}
    with open("static/test/ifias_1.json") as f:
        d = json.load(f)
    f.close()
    print(get_info(d))
    print('end: ', time.time())
    # url = 'https://source.cmc.zucc.edu.cn/uploads/2022/Sep/202209201521421h226f2m7mz0.docx'
    # print(get_info(url))
