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
    def __init__(self, detect_model = 'yolo11l.pt', seg_model = 'yolo11l-seg.pt'):
        self.detect_model = YOLO(detect_model).to(device)
        self.seg_model = YOLO(seg_model).to(device)
    def __init__(self, model_selection = 'yolo11l.pt'):
        self.model = YOLO('yolo11l.pt').to(device)
        self.results = None
        self.cls_counts = {}
    def __detect__(self, frame):
        """单纯检测图像中的物体，返回检测后的图像"""
        self.results = self.detect_model(frame)
        annotated_frame = self.results[0].plot()
        return annotated_frame
    def __segmentation__(self, frame):
        """对检测到的物体进行分割，返回分割后的图像"""
        self.results = self.seg_model(frame)
        frame_resized = cv2.resize(frame, (640, 640))
        self.results = self.model(frame)
        annotated_frame = self.results[0].plot()
        return annotated_frame
    def __count__(self):
        """统计检测到的物体类别名称以及数量"""
        result = self.results[0]
        self.cls_counts = {}
        for box in result.boxes:
            cls_index = (box.cls.item()) 
            cls_name = result.names[cls_index]
            if cls_name not in self.cls_counts:
                self.cls_counts[cls_name] = 1
            else:
                self.cls_counts[cls_name] += 1
        return self.cls_counts