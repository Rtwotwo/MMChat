"""
Author: Redal
Date: 2025/03/31
TODO: 设计一个基于语音文本转换的交互软件,包括语言视觉模型
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import cv2
import threading
import queue
import tkinter as tk
from PIL import Image, ImageTk
from utils.plot_sub import ComputeHistogramImage
from utils.plot_sub import CalculateSpectrogramImage


class ModelChatApp(tk.Frame):
    """针对语音文本以及视觉的交互模型界面,用于使用VLM模型分析实际场景,
    并通过文本转换语音来进行播放,设置一系列按钮进行控制播放与否以及模型的选择
    主要包括模型internlm/deepseek/llava等模型的使用"""
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.__set_widgets__()
        self.video_cap = cv2.VideoCapture(0)
        self.threading = threading.Thread(target=self.__video_loop__)
        self.threading.daemon = True
        self.threading.start()
        self.queue = queue.Queue()
    def __set_widgets__(self):
        """设置界面组件与整体布局"""
        self.root.title('MMChat-Redal-ModelChatApp')
        self.root.geometry('800x600')
        # 设置实时视频播放的相关的组件
        self.video_label = tk.Label(self.root, font=('Arial', 8), width=500, height=400, 
                            fg='black', bg='white', justify='center', wraplength='200')
        self.video_label.place(x=0, y=0)
        self.histogram_label = tk.Label(self.root, font=('Arial', 8), width=300, height=200,
                            fg='black', bg='white', justify='center', wraplength='200')
        self.histogram_label.place(x=0, y=400)
        self.spectrogram_label = tk.Label(self.root, font=('Arial', 8), width=200, height=200,
                            fg='black', bg='white', justify='center', wraplength='200') 
        self.spectrogram_label.place(x=300, y=400)
        # 设置模型交互的相关组件
        self.chat_label = tk.Label(self.root, font=('Arial', 8), width=200, height=400, 
                            fg='black', bg='white', justify='center', wraplength='200')
        self.chat_label.config(text='你好,欢迎使用MMChat-ModelChatApp')
        self.chat_label.place(x=500, y=0)
        self.entry_mess = tk.Entry(self.root, font=('Arial', 8), width=20)
        self.entry_mess.place(x=500, y=400)
    def __video_loop__(self):
        while self.video_cap.isOpened():
            ret, frame = self.video_cap.read()
            frame = cv2.flip( cv2.resize( cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (500,400) ), 1)
            if ret: 
                self.frame = frame
                self.__video_show__()
            else:break
    def __video_show__(self):
        image_tk = ImageTk.PhotoImage(Image.fromarray(self.frame))
        image_hist_tk = ImageTk.PhotoImage(Image.fromarray(ComputeHistogramImage(self.frame)))
        image_freq_tk = ImageTk.PhotoImage(Image.fromarray(CalculateSpectrogramImage(self.frame)))
        self.video_label.config(image=image_tk)
        self.histogram_label.config(image=image_hist_tk)
        self.spectrogram_label.config(image=image_freq_tk)
        self.video_label.image = image_tk
        self.histogram_label.image = image_hist_tk
        self.spectrogram_label.image = image_freq_tk
        self.after(10)


if __name__ == '__main__':
    root = tk.Tk()
    app = ModelChatApp(root)
    app.mainloop()
