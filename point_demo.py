import argparse

import numpy as np
import mmcv
import glob
from opera.apis import init_detector, inference_detector
from opera.infence import find_teacher, point


def main(img_path=None):
    # load model
    config_file = 'opera/configs/inspose/inspose_r50_8x4_3x_coco.py'
    checkpoint_file = 'opera/configs/inspose/inspose_r50_8x4_36e_coco.pth'
    model = init_detector(config_file, checkpoint_file, device='cuda:0')
    # load img
    # path = 'img/18832_643_6_1_2_11_4_1,2_C21025.jpg'
    path = 'img/9483_5074_10_8_48_7_4_1,2_J02012.jpg'
    if img_path is not None:
        path = img_path
    img = mmcv.imread(path)
    # name file
    file_name = 2
    # infence
    result, img = point(model, img, file_name)
    # result = [num, path]
    if result is None:
        print('no person')
        return
    print(result)
    path = '/home/amax/haidongxu/python/point/' + str(3) + '.png'
    mmcv.imwrite(img, path)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-path', type=str, help='image path')
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    main(**vars(opt))
