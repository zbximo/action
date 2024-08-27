import copy
import numpy as np

import mmcv
from opera.apis import init_detector, inference_detector


def find_teacher(model, ori_img):
    img = copy.deepcopy(ori_img)
    result = inference_detector(model, img)
    score_thr = 0.3
    img = img.astype(np.uint8)
    img = mmcv.bgr2rgb(img)
    width, height = img.shape[1], img.shape[0]
    bbox_result, keypoint_result = result
    bboxes = np.vstack(bbox_result)
    keypoints = np.vstack(keypoint_result)
    scores = bboxes[:, -1]
    inds = scores > score_thr
    bboxes = bboxes[inds, :]
    keypoints = keypoints[inds, ...]
    num = keypoints.shape[0]
    if num == 0:
        return None
    teacher = 0
    for i, kpt in enumerate(keypoints):
        if kpt[0][1] < keypoints[teacher][0][1]:
            teacher = i
    teacher = keypoints[teacher]
    hip = teacher[11][1] + teacher[12][1] / 2
    knee = teacher[13][1] + teacher[14][1] / 2
    ankle = teacher[15][1] + teacher[16][1] / 2
    if (knee - hip) > (ankle - knee) * 0.8:
        state = 'stand'
    else:
        state = 'sit'
    if (teacher[1][0] - teacher[2][0]) > (teacher[5][0] - teacher[6][0]) * 0.4:
        direction = 'side'
    elif teacher[1][0] < teacher[2][0]:
        direction = 'back'
    else:
        direction = 'front'
    writing = 'speaking'
    if state == 'stand' and (direction == 'side' or direction == 'back'):
        if teacher[7][1] > teacher[9][1] or teacher[8][1] > teacher[10][1]:
            writing = 'writing'
    if state == 'sit' and direction == 'back':
        return None
    return [state, direction, writing, teacher[5][0], teacher[6][0]]
