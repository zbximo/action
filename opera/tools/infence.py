import argparse
import numpy as np
import mmcv
import glob
from opera.apis import init_detector, inference_detector
from opera.infence import find_teacher, stu_point

config_file = 'opera/configs/petr/petr_swin-l-p4-w7-224-22kto1k_16x1_100e_crowdpose.py'
checkpoint_file = 'opera/configs/petr/petr_swin-l-p4-w7-_16x1_100e_crowdpose.pth'
model = init_detector(config_file, checkpoint_file, device='cuda:1')
# load img
file_name = "/home/amax/haidongxu/python/static/student.jpg"
img = mmcv.imread(file_name)
# infence
result = stu_point(model, img, file_name)
print(result[0])
