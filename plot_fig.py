# -*- encoding: utf-8 -*-
# @ModuleName: plot_fig
# @Function :
# @Author : ximo
# @Time : 2022/9/19 15:19
import datetime
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# plt.rcParams['font.family'] = ['sans-serif']
# plt.rcParams['font.sans-serif'] = ['SimHei']
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
# 引入结巴库
import jieba
# 词云库
from wordcloud import WordCloud, STOPWORDS
# import matplotlib.pyplot as plt
# from PIL import Image  # 处理图片的
# # 协助处理图片
from util import create_dic


def get_met(seq):
    # print(seq)
    data = np.zeros((15, 15))
    # seq_ = np.array(seq)
    seq = np.array(seq)
    seq_ = np.where(seq >= 5, seq - 1, seq)
    # print(seq_)
    for i in range(len(seq_) - 1):
        x = seq_[i] - 1
        y = seq_[i + 1] - 1
        data[x, y] += 1
        data[x, -1] += 1
        data[-1, y] += 1
        data[-1, -1] += 1
    return data.astype(int)


def plot_ifias(data, file_name):
    # print(data)
    dic_path = create_dic('ifias')
    data = get_met(data)
    # print(data)
    data_list = data[:-1, :-1].flatten().tolist()
    data_sort = np.sort(data_list)
    max = data_sort[-2] * 1.5 if data_sort[-1] > data_sort[-2] * 1.5 else data_sort[-1]
    normal = cm.colors.Normalize(min(data_list), max)
    bcmap2 = plt.cm.cool(normal(data_list), alpha=0.8)
    # print('d', data.tolist())
    fig = plt.figure()

    # plt.gca().xaxis.set_major_locator(plt.NullLocator())
    # plt.gca().yaxis.set_major_locator(plt.NullLocator())
    # plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    # plt.margins(0, 0)
    ax = fig.add_subplot()
    rowLabels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "Total"]
    rowColours = ["#F0C9C0"] * 15
    colColors = ["#00ccff"] * 15
    column_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "Total"]
    # 取消坐标轴
    ax.axis('off')
    table = ax.table(cellText=data,
                     colLabels=column_labels,
                     colColours=colColors,
                     rowColours=rowColours,
                     rowLabels=rowLabels,
                     cellLoc='center',
                     rowLoc='center',
                     colLoc='center',
                     loc="center",
                     )
    table.auto_set_font_size(True)
    table.scale(1, 1)
    for idx, bb in enumerate(bcmap2):
        table[idx // 14 + 1, idx % 14].set_facecolor(bb)
    # table.set_fontsize(10)
    path = os.path.join(dic_path, file_name + '.png')
    print(path)
    plt.savefig(path, format='png', bbox_inches='tight', transparent=True, pad_inches=0)

    # ABCD区域
    A = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]
    B = [[7, 6], [7, 7], [8, 6], [8, 7]]
    C = [[4, 4], [4, 5], [5, 4], [5, 5]]
    D = [[8, 8], [8, 9], [8, 10], [9, 8], [9, 9], [9, 10], [10, 8], [10, 9], [10, 10]]
    # list_area = []
    # list_area.extend(A)
    # list_area.extend(B)
    # list_area.extend(C)
    # list_area.extend(D)
    fig = plt.figure()
    ax = fig.add_subplot()
    rowLabels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "Total"]
    rowColours = ["#F0C9C0"] * 15
    colColors = ["#00ccff"] * 15
    column_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "Total"]
    # 取消坐标轴
    ax.axis('off')
    table = ax.table(cellText=data,
                     colLabels=column_labels,
                     colColours=colColors,
                     rowColours=rowColours,
                     rowLabels=rowLabels,
                     cellLoc='center',
                     rowLoc='center',
                     colLoc='center',
                     loc="center",
                     )
    table.auto_set_font_size(True)
    table.scale(1, 1)
    legend_elements = [Patch(facecolor='#dbf1d1', edgecolor='#dbf1d1',
                             label='A'),
                       Patch(facecolor='#81e654', edgecolor='#81e654',
                             label='B'),
                       Patch(facecolor='#94a48d', edgecolor='#94a48d',
                             label='C'),
                       Patch(facecolor='#3a9e0e', edgecolor='#3a9e0e',
                             label='D')
                       ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1., 0.5))
    for i in A:
        table[i[0], i[1] - 1].set_facecolor('#dbf1d1')
    for i in B:
        table[i[0], i[1] - 1].set_facecolor('#81e654')
    for i in C:
        table[i[0], i[1] - 1].set_facecolor('#94a48d')
    for i in D:
        table[i[0], i[1] - 1].set_facecolor('#3a9e0e')
    path2 = os.path.join(dic_path, file_name + '_area.png')
    print(path2)
    plt.savefig(path2, format='png', bbox_inches='tight', transparent=True, pad_inches=0)

    return path, path2
    # plt.show()


def get_word_cloud(data, file_name):
    # f = open('static/stopwords.txt', 'r', encoding='utf-8')
    # stop_words = f.read()
    # f.close()
    stopwords = set()
    content = [line.strip() for line in open('static/stopwords.txt', 'r').readlines()]
    stopwords.update(content)

    txt = "".join(data)
    # 使用精确模式对文本进行分词
    words = jieba.lcut(txt)
    # print(words)
    # 通过键值对的形式存储词语及其出现的次数
    # 大括号表示 python的字典类型对应，
    counts = {}
    # 数组对象  用来接收需要传递给词云的内容
    chiyun = []
    for word in words:
        # == 1 单个词语不计算在内
        if len(word) < 2:
            continue
        else:
            # 遍历所有词语，每出现一次其对应的值加 1
            counts[word] = counts.get(word, 0) + 1

    # 将键值对转换成列表
    items = list(counts.items())

    # 根据词语出现的次数对字典进行lambda匿名排序
    items.sort(key=lambda x: x[1], reverse=True)
    # 列标题 format
    # print("{0:<5}{1:<8}{2:<5}".format('序号', '词语', '频率'))

    for i in range(len(items)):
        word, count = items[i]
        # print("{0:<5}{1:<8}{2:>5}".format(i + 1, word, count))
        chiyun.append(word)
    # print(len(chiyun))
    # print(chiyun)
    # 加载背景图片信息
    # maskph = cv2.imread("static/school_emblem.png")

    # join 函数 用斜杆拼接词组
    text_cut = '/'.join(chiyun)
    try:
        wordcloud = WordCloud(font_path="static/SimHei.ttf", background_color='white', stopwords=stopwords,
                              width=1000, height=860, margin=2,
                              scale=4).generate(text_cut)
    except:
        return None
    # 显示图片
    dic_path = create_dic('wordcloud')
    # print(dic_path)
    path = os.path.join(dic_path, file_name + ".png")
    wordcloud.to_file(path)  # 保存成图片
    return path
    # plt.imshow(wordcloud)
    # plt.axis('off')
    # plt.show()


if __name__ == '__main__':
    data = [1] * 256
    plot_ifias(data, '11')
