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
from models.llm_chat_model import ollama_generator
from models.llm_chat_model import llm_chat
from utils.plot_sub import ComputeHistogramImage
from utils.plot_sub import CalculateSpectrogramImage


class ModelChatApp(tk.Frame):
    """针对语音文本以及视觉的交互模型界面,用于使用VLM模型分析实际场景,
    并通过文本转换语音来进行播放,设置一系列按钮进行控制播放与否以及模型的选择
    主要包括模型internlm/deepseek/llava等模型的使用"""
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.__set_cached__()
        self.__set_widgets__()
        self.queue = queue.Queue()
    def __set_cached__(self):
        """设置相关变量缓存"""
        self.video_cap = None
        self.prompt = None
        self.triggle_video_flag = False
        cover = cv2.resize( cv2.imread('assets/MMChat_logo.jpg'), (500,400) )
        self.frame = cover
        self.cover_imgtk = ImageTk.PhotoImage( Image.fromarray( cover) )
    def __set_widgets__(self):
        """设置界面组件与整体布局"""
        self.root.title('MMChat-Redal-ModelChatApp')
        self.root.geometry('800x600')
        # 设置实时视频播放的相关的组件
        self.video_label = tk.Label(self.root, font=('Arial', 8), width=500, height=400, 
                            fg='black', bg='white', justify='center', wraplength='200')
        self.video_label.place(x=0, y=0)
        self.video_label.config(image=self.cover_imgtk)
        self.video_label.image = self.cover_imgtk
        self.histogram_label = tk.Label(self.root, font=('Arial', 8), width=300, height=200,
                            fg='black', bg='white', justify='center', wraplength='200')
        self.histogram_label.place(x=0, y=400)
        self.spectrogram_label = tk.Label(self.root, font=('Arial', 8), width=200, height=200,
                            fg='black', bg='white', justify='center', wraplength='200') 
        self.spectrogram_label.place(x=300, y=400)
        # 设置模型交互的相关组件
        self.chat_text = tk.Text(self.root, font=('Arial', 8), bg='white', width=40, height=27)
        self.chat_text.place(x=505, y=0)
        self.chat_text.insert(tk.END,'欢迎使用MMChat-ModelChatApp\n', 'center')
        self.chat_text.tag_configure('center', justify='center')
        self.entry_mess = tk.Entry(self.root, font=('Arial', 8), width=30)
        self.entry_mess.place(x=505, y=384)
        self.sendchat_button = tk.Button(self.root, text='发送信息', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__send_chat__)
        self.sendchat_button.place(x=680, y=382)
        self.audio_chat_button = tk.Button(self.root, text='语音聊天', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__send_chat__)
        self.audio_chat_button.place(x=505, y=405)
        # 相关按钮组件
        self.triggle_video_button = tk.Button(self.root, text='播放视频', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__start_video__)
        self.triggle_video_button.place(x=505, y=430)
        self.exit_button = tk.Button(self.root, text='退出', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__exit__)
        self.exit_button.place(x=505, y=455)
        
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

    def __send_chat__(self):
        """用户发送聊天信息给聊天框,信息居右"""
        self.prompt = self.entry_mess.get()
        self.chat_text.insert(tk.END, '\n'+self.entry_mess.get(), 'right_red')
        self.chat_text.tag_configure('right_red', justify='right', foreground='red')
        self.entry_mess.delete(0, tk.END)
        self.chat_text.see(tk.END)
        # show response
        self.chat_text.insert(tk.END, '\n'+llm_chat(self.prompt), 'left_blue')
        self.chat_text.tag_configure('left_blue', justify='left', foreground='blue')
        self.chat_text.see(tk.END)
    def __start_video__(self):
        """播放视频,并开启视频线程"""
        self.triggle_video_flag = not self.triggle_video_flag
        if self.triggle_video_flag:
            self.video_cap = cv2.VideoCapture(0)
            self.video_thread = threading.Thread(target=self.__video_loop__)
            self.video_thread.start()
        else: 
            self.video_label.config(image=self.cover_imgtk)
            self.video_label.image = self.cover_imgtk
            self.video_cap.release()
    def __exit__(self):
        """退出程序,清除缓存以及资源""" 
        if self.video_cap is not None:
            self.video_cap.release()
        self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = ModelChatApp(root)
    app.mainloop()
