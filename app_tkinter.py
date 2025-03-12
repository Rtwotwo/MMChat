"""
任务: 多模态语音、视觉、手势模型的搭建
      并且构建tkinter的GUI界面框架
时间: 2025/03/03-Redal
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



########################  构造基本GUI界面框架  ###########################
class ChatMMGUI(tk.Frame):
      """The GUI is designed to interact with multi_models tkinter"""
      def __init__(self, root):
            super().__init__(root)
            self.root = root

      
      def __widgets__(self):
            self.root.title('ChatMMGUI - Redal')
            self.root.geometry('800x600')
            

