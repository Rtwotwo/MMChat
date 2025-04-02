"""
Author: Redal
Date: 2025/04/01
TODO: MMChat utils directory yolo_detect.py
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import cv2
import torch
from ultralytics import YOLO
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class ObjectDetect(object):
    def __init__(self, model_selection = 'yolo11l.pt'):
        self.model = YOLO('yolo11l.pt').to(device)
    def __detect__(self, frame):
        """单纯检测图像中的物体，返回检测后的图像"""
        frame_resized = cv2.resize(frame, (640, 640))
        results = self.model(frame)
        annotated_frame = results[0].plot()
        return annotated_frame
    # def __



if __name__ == '__main__':
    od = ObjectDetect()
    frame = cv2.imread(r'assets\face_cls\multi_face.jpg')
    result = od.__detect__(frame)
    cv2.imwrite('image_content/test.jpg', result)