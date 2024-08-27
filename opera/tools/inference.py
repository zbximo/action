import argparse
import numpy as np
import mmcv
import glob
from opera.apis import init_detector, inference_detector
from opera.infence import find_teacher, point

config_file = 'opera/configs/inspose/inspose_r50_8x4_3x_coco.py'
checkpoint_file = 'opera/configs/inspose/inspose_r50_8x4_36e_coco.pth'
model = init_detector(config_file, checkpoint_file, device='cuda:1')
# load img
file_name = "/home/amax/haidongxu/python/static/a3.jpg"
img = mmcv.imread(file_name)
# infence
result = point(model, img, file_name)
print(result[0])
