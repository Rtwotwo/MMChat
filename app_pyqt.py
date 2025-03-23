"""
Author: Redal
Date: 2025/03/03
TODO: 多模态语音、视觉、手势模型的搭建, 并且构建tkinter的GUI界面框架
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import sys
import cv2
import torch
import argparse
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from models.face_cls_model import FaceNetExtractor

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")



##########################  定义变量解析阈  #############################
def pyqt_config():
    parser = argparse.ArgumentParser(description='PyQt_GUI related arguments definition',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)



##########################  PyQt_GUI软件设计  #############################
class MMChat_PyQt(QMainWindow):
    def __init__(self, args, **kwargs):
        super().__init__()
        self.set_widgets()
    def set_widgets(self):
        self.setWindowTitle("MMChat-Redal")
        self.setGeometry(500, 100, 800, 600)

    
##########################  主函数测试分析  #############################
if __name__ == "__main__":
    """Test the PyQt GUI"""
    args = pyqt_config()
    # Initialize PyQt GUI
    app = QApplication(sys.argv)
    window = MMChat_PyQt(args)
    window.show()
    sys.exit(app.exec_())