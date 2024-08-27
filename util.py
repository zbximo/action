# -*- encoding: utf-8 -*-
# @ModuleName: util
# @Function :
# @Author : ximo
# @Time : 2022/10/31 15:25
from datetime import date

import cv2
import numpy as np
import os


def judge_blur_img(img):
    """
    取最下面一行为参照。
    从下往上遍历，出现5次差值过大的情况，即停止，记录index。
    if index > 0.5*h，则返回404
    elif index > 0.15*h, 则predict。
        if predict is None:
            return 模糊
        else
            return result
    else return 模糊
    :param img: 灰度图
    :return:
    """
    img = img.astype(np.float32)
    h, w = img.shape[0], img.shape[1]
    refer = img[-1]
    cnt = 0
    index = 0
    for i in range(h - 1, 0, -1):
        index += 1
        d = np.abs(refer - img[i - 1])
        if np.max(d) >= 15:
            cnt += 1
        if cnt >= 5:
            return 1.0 * index / h


def remove_wav(file_path):
    os.remove(file_path)


def is404(img_np):
    img = cv2.imread('static/404.jpg')
    # print(444)
    if img.shape[0] != img_np.shape[0] or img.shape[1] != img_np.shape[1]:
        return False
    if (img == img_np).all():
        return True
    else:
        return False


def create_dic(name):
    """

    :param name: 接口(student ifias)
    :return:
    """

    time = date.today()
    if name == 'student':
        dic_path = 'static/student_point/' + str(time.year) + '/' + str(time.month) + '/' + str(time.day)
    elif name == 'ifias':
        dic_path = 'static/ifias_png/' + str(time.year) + '/' + str(time.month) + '/' + str(time.day)
    elif name == 'wordcloud':
        dic_path = 'static/wordcloud/' + str(time.year) + '/' + str(time.month) + '/' + str(time.day)
    else:
        raise "Error"
    if not os.path.exists(dic_path):
        os.makedirs(dic_path)
    return dic_path


if __name__ == '__main__':
    create_dic('student')
    blur_file = ["08551dac-abe5-49b8-9394-332581cf54e7_20221030145906A878.jpg",
                 "c120e84c-22fc-43c8-91fe-9f9f8ac76dbb_20221030152508A355.jpg",
                 "c746ec3f-d93e-4922-b284-12b935def01d_20221030154703A962.jpg"]
    file = ['c54f887f-521a-42c0-9cf0-948881ec9352_20221030153306A582.jpg',
            "cc63dd51-b242-43bc-a523-93af12b635e1_20221030152111A244.jpg"
            ]
    for i in file:
        img = cv2.imread("blur_img/" + i, 0)
        print(judge_blur_img(img))