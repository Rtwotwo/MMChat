"""
Author: Redal
Date: 2025/03/03
TODO: 多模态语音、视觉、手势模型的搭建, 并且构建tkinter的GUI界面框架
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import sys
import cv2
import argparse
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QCamera, QCameraInfo, QCameraViewfinderSettings
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)



##########################  定义变量解析阈  #############################
def pyqt_config():
    parser = argparse.ArgumentParser(description='PyQt_GUI related arguments definition',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--main_window_title', type=str, default='MMChat-Redal', help='The title of the PyQt_GUI window')
    parser.add_argument('--main_window_ulx', type=int, default=100, help='The upper left x coordinate of the PyQt_GUI window')
    parser.add_argument('--main_window_uly', type=int, default=100, help='The upper left y coordinate of the PyQt_GUI window')
    parser.add_argument('--main_window_width', type=int, default=800, help='The width of the PyQt_GUI window')
    parser.add_argument('--main_window_height', type=int, default=600, help='The height of the PyQt_GUI window')
    args = parser.parse_args()
    return args



##########################  PyQt_GUI软件设计  #############################
class MMChatPyQt(QMainWindow):
    def __init__(self, args, **kwargs):
        super().__init__()
        self.args = args
        self.set_widgets()
    def set_widgets(self):
        self.setWindowTitle(self.args.main_window_title)
        self.setGeometry(self.args.main_window_ulx, self.args.main_window_uly,
                         self.args.main_window_width, self.args.main_window_height)
        # Create video display widget
        


##########################  主函数测试分析  #############################
if __name__ == "__main__":
    """Test the PyQt GUI"""
    args = pyqt_config()
    # Initialize PyQt GUI
    app = QApplication(sys.argv)
    window = MMChatPyQt(args)
    window.show()
    sys.exit(app.exec_())