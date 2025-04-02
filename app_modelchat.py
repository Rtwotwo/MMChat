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
from models.audio_text_conversion import audio_text_config
from models.audio_text_conversion import audio_recording
from models.audio_text_conversion import save_audiodata
from models.audio_text_conversion import audio_to_text
from utils.plot_sub import ComputeHistogramImage
from utils.plot_sub import CalculateSpectrogramImage
from utils.plot_sub import GifPlayer
from utils.object_detect import ObjectDetect


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
        self.filename = 'assets/audio_gif/dynamic1.gif'
        self.frame = None
        self.prompt = None
        self.video_cap = None
        self.screen_shot_frame = None
        self.over_video_label = None
        self.triggle_video_flag = False
        self.gif_player_flag = False
        self.object_detect_flag = False
        cover = cv2.resize( cv2.imread('assets/MMChat_logo.jpg'), (500,400) )
        self.frame = cover
        self.obd = ObjectDetect()
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
        # 创建组件self.over_screen_shot_label组件
        self.over_video_label = tk.Label(self.root, font=('Arial', 8), width=100, height=100,
                        fg='black', bg='white', justify='center', wraplength='200')
        self.over_video_label.place_forget()
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
        self.sendchat_button.place(x=680, y=380)
        # 相关按钮组件->第一行相关按钮
        self.audio_chat_button = tk.Button(self.root, text='语音聊天', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__audio_chat__)
        self.audio_chat_button.place(x=505, y=405)
        self.image_chat_button = tk.Button(self.root, text='图片交流', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__send_chat__)
        self.image_chat_button.place(x=593, y=405)
        self.message_clear_button = tk.Button(self.root, text='清空聊天', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__clear_message__)
        self.message_clear_button.place(x=680, y=405)
        # 相关按钮组件->第二行相关按钮
        self.triggle_video_button = tk.Button(self.root, text='播放视频', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__start_video__)
        self.triggle_video_button.place(x=505, y=430)
        self.screen_shot_button = tk.Button(self.root, text='截取视频', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__screen_shot__)
        self.screen_shot_button.place(x=593, y=430)
        self.clear_shot_button = tk.Button(self.root, text='清除截图', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__clear_shot__)
        self.clear_shot_button.place(x=680, y=430)
        # 相关按钮组件->第三行相关按钮
        self.object_detect_button = tk.Button(self.root, text='物体检测', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__object_detect__)
        self.object_detect_button.place(x=505, y=455)
        self.exit_button = tk.Button(self.root, text='退出系统', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__exit__)
        self.exit_button.place(x=680, y=455)        
    def __video_loop__(self):
        while self.video_cap.isOpened():
            ret, frame = self.video_cap.read()
            frame = cv2.flip( cv2.resize( cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (500,400) ), 1)
            if ret: 
                self.frame = frame
                if self.object_detect_flag: 
                    self.frame = self.obd.__detect__(self.frame)
                    # print(self.obd.__count__())
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
        if not self.video_cap.isOpened():
            self.video_label.config(image=self.cover_imgtk)
            self.video_label.image = self.cover_imgtk
        self.after(10)
    def __send_chat__(self):
        """用户发送聊天信息给聊天框,信息居右"""
        self.prompt = self.entry_mess.get()
        self.chat_text.insert(tk.END, '\n'+self.entry_mess.get(), 'right_red')
        self.chat_text.tag_configure('right_red', justify='right', foreground='red')
        self.entry_mess.delete(0, tk.END)
        self.chat_text.see(tk.END)
        # 显示来自 LLM 模型的响应
        if self.prompt:
            threading.Thread(target=self.__llmchat_response__, daemon=True).start()
            
    def __llmchat_response__(self):
        """LLM模型响应,单独开启增加线程实现并发"""
        self.chat_text.insert(tk.END, '\n'+ollama_generator(self.prompt), 'left_blue')
        self.chat_text.tag_configure('left_blue', justify='left', foreground='blue')
        self.chat_text.see(tk.END)
    def __clear_message__(self):
        """清空聊天框"""
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.insert(tk.END, '欢迎使用MMChat-ModelChatApp\n', 'center')
        self.chat_text.tag_configure('center', justify='center')
    def __start_video__(self):
        """播放视频,并开启视频线程"""
        self.triggle_video_flag = not self.triggle_video_flag
        if self.triggle_video_flag:
            self.video_cap = cv2.VideoCapture(0)
            self.video_thread = threading.Thread(target=self.__video_loop__)
            self.video_thread.daemon = True
            self.video_thread.start()
        else: self.video_cap.release()
    def __audio_chat__(self):
        """构建语音聊天功能"""
        self.gif_player_flag = not self.gif_player_flag
        if self.gif_player_flag:
            # 播放Gif动画
            self.gifplayer = GifPlayer(self.root, self.video_label, self.filename)            
        else:
            self.gifplayer.__stop__()
            self.video_label.config(image=self.cover_imgtk)
            self.video_label.image = self.cover_imgtk
    def __screen_shot__(self):
        """截取视频并保存为图片,并在over_video_label中展示"""
        if self.video_cap is not None:
            self.over_video_label.place(x=400, y=300)
            # 截取视频帧
            self.screen_shot_frame = cv2.resize( self.frame, (100,100) )
            self.screen_shot_imgtk = ImageTk.PhotoImage(Image.fromarray(self.screen_shot_frame))
            self.over_video_label.config(image=self.screen_shot_imgtk)
            self.over_video_label.image = self.screen_shot_imgtk
        else:
            # 隐藏上显示label
            self.over_video_label.place_forget()
    def __clear_shot__(self):
        """清除截图销毁over_video_label组件"""
        if self.over_video_label is not None:
            self.over_video_label.place_forget()
    def __object_detect__(self):
        """使用YOLOv11进行物体检测"""
        if self.video_cap:
            self.object_detect_flag = not self.object_detect_flag
    def __exit__(self):
        """退出程序,清除缓存以及资源""" 
        if self.video_cap is not None:
            self.video_cap.release()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = ModelChatApp(root)
    app.mainloop()
