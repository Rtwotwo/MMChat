"""
Author: Redal
Date: 2025/03/03
TODO: 多模态语音、视觉、手势模型的搭建, 并且构建tkinter的GUI界面框架
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import sys
import argparse
import threading
import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import torch
import torch.functional as F
from torchvision.transforms import transforms

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')



########################  配置tkinter的界面配置  ###########################
def GUI_Config():
      """The GUI is defined for tkinter configuration"""
      parser = argparse.ArgumentParser(description='MMChat GUI configuration',
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
      parser.add_argument('--gui_title', type=str, default='MMChat', help='The title of the GUI window')
      parser.add_argument('--gui_width', type=str, default='800', help='The width of the GUI window')
      parser.add_argument('--gui_height', type=str, default='600', help='The height of the GUI window')
      parser.add_argument('--audio_shower', type=str, default='assets/audio_gif/dynamic1.gif', help='The audio shower of the GUI window')
      args = parser.parse_args()
      return args



########################  构造基本GUI界面框架  ###########################
class ChatMMGUI(tk.Frame):
      """The GUI is designed to interact with multi_models tkinter"""
      def __init__(self, root, args):
            super().__init__(root)
            self.root = root
            self.args = args
            self.__widgets__()
      
      def __widgets__(self):
            self.root.title('ChatMMGUI-Redal')
            self.root.geometry(f'{self.args.gui_width}x{self.args.gui_height}')
            self.main_label = tk.Label(self.root); self.main_label.place(x=0, y=0)
            self.main_label.config()
            



########################  主函数测试分析  ###########################
if __name__ == '__main__':
      args = GUI_Config()
      root = tk.Tk()
      root.mainloop()
            

