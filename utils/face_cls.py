"""
Author: Redal
Date: 2025/03/24
TODO: Face Authorization 
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import cv2
from facenet_pytorch import MTCNN


def FaceVisiblity(frame):
    """make the main face visible and plot bounding box
    :param frame: the camera frame to de ploted"""
    mtcnn = MTCNN(image_size=512, margin=0, keep_all=False, post_process=True)
    boxes, _ = mtcnn.detect(frame, landmarks=False)
    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = box.astype(int)
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return frame
    else: return frame


def DeciderCenter(frame, r_pixels = 50):
    """make the main face visible and plot bounding box
    :param frame: the camera frame to de ploted
    :return: bool value for answer whether center or not"""
    mtcnn = MTCNN(image_size=512, margin=0, keep_all=False, post_process=True)
    boxes, _ = mtcnn.detect(frame, landmarks=False)
    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = box.astype(int)
            

