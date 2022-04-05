from itertools import count
import time
from random import randint
import logging

import cv2 as cv
from mmdet.apis import init_detector, inference_detector, show_result_pyplot
from mmpose.apis import init_pose_model, inference_top_down_pose_model, process_mmdet_results, vis_pose_result
import mmcv
import numpy as np
import requests
from requests import ConnectionError, Timeout, HTTPError

from rumpleteazer.util.logging import get_logger


def run():
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        logger.error('could not open video capture')
        exit()

    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

    # model
    # det_config = '/home/antares/Documents/github/mmdetection/configs/yolof/yolof_r50_c5_8x8_1x_coco.py'
    # det_checkpoint = ('/home/antares/Documents/code/'
    #                   'Rumpleteazer/rumpleteazer/checkpoints/yolof_r50_c5_8x8_1x_coco_20210425_024427-8e864411.pth')
    det_config = '/home/antares/Documents/github/mmdetection/work_dirs/yolof_finetune_1000_epoch/yolof_finetune.py'
    det_checkpoint = '/home/antares/Documents/github/mmdetection/work_dirs/yolof_finetune_1000_epoch/epoch_1000.pth'
    pose_config = ('/home/antares/Documents/github/'
                   'mmpose/configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/litehrnet_30_coco_384x288.py')
    pose_checkpoint = ('/home/antares/Documents/code/'
                       'Rumpleteazer/rumpleteazer/checkpoints/litehrnet30_coco_384x288-a3aef5c4_20210626.pth')

    # build the model from a config file and a checkpoint file
    det_model = init_detector(det_config, det_checkpoint, device='cuda:0')
    pose_model = init_pose_model(pose_config, pose_checkpoint, device='cuda:0')

    # # Create MultiTracker object
    # tracker = cv.legacy.MultiTracker_create()

    for index in count(0):
        tic = time.time()

        # Capture frame-by-frame
        successful, frame = capture.read()
        if not successful:
            logger.error('failed to get frame. Exiting ...')
            break

        # detection model inference
        det_results = inference_detector(det_model, frame)
        person_results = process_mmdet_results(det_results, cat_id=1)  # cat_id (int): default: 1 for human

        # pose model inference
        pose_results, returned_outputs = inference_top_down_pose_model(pose_model,
                                                                       frame,
                                                                       person_results=person_results,
                                                                       format='xyxy',
                                                                       bbox_thr=0.5)

        # image = det_model.show_result(
        #     frame,
        #     det_results,
        #     show=False,
        #     bbox_color=(72, 101, 241),
        #     text_color=(72, 101, 241)
        # )
        image = vis_pose_result(pose_model,
                                frame,
                                pose_results,
                                dataset='TopDownCocoDataset',
                                show=False)

        cv.imshow('frame', image)

        # pre-processing results
        output = []
        for result in pose_results:
            # find head position (if possible)
            keypoints = result['keypoints'][:5, :]  # nose, left_eye, right_eye, left_ear, right_ear
            head_x, head_y, head_prob = np.mean(keypoints, axis=0)
            if head_prob > 0.6:
                output.append([head_x.item(), head_y.item()])
                continue

            # use bbox center
            bbox_x1, bbox_y1, bbox_x2, bbox_y2, bbox_prob = result['bbox']
            center_x = np.mean([bbox_x1, bbox_x2])
            center_y = np.mean([bbox_y1, bbox_y2])
            output.append([center_x.item(), center_y.item()])

        try:
            requests.post('http://192.168.0.19:7777',
                          json=output,
                          timeout=0.1)
        except (ConnectionError, Timeout, HTTPError) as e:
            logger.error(e)

        toc = time.time()
        logger.info(f'frame {index}: {toc - tic}s')

        if cv.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    capture.release()
    cv.destroyAllWindows()


def main():
    run()


if __name__ == '__main__':
    logger = get_logger(name=__name__)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    main()
