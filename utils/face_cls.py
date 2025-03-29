"""
Author: Redal
Date: 2025/03/24
TODO: Face Authorization 
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import cv2
import math


def FaceVisiblity(mtcnn, frame):
    """make the main face visible and plot bounding box
    :param frame: the camera frame to de ploted"""
    boxes, _ = mtcnn.detect(frame, landmarks=False)
    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = box.astype(int)
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return frame
    else: return frame


def DeciderCenter(mtcnn, frame, r_pixels = 100):
    """make the main face visible and plot bounding box
    :param frame: the camera frame to de ploted
    :return: bool value for answer whether center or not
    and the chenter os frame is (256,256)"""
    boxes, _ = mtcnn.detect(frame, landmarks=False)
    if boxes is not None:
        for box in boxes:
            # Choose the first face for decider
            x1, y1, x2, y2 = box.astype(int)
            center_x, center_y = (x1+x2)//2, (y1+y2)//2
            abs_dis = math.sqrt(  (center_x-256)**2 + (center_y-256)**2)
            if abs_dis < r_pixels: return True
    else: return False