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
from models.audio_text_conversion import text_to_audio
from utils.plot_sub import ComputeHistogramImage
from utils.plot_sub import CalculateSpectrogramImage
from utils.plot_sub import GifPlayer
from utils.object_detect import ObjectDetect
from utils.vlm_prompt import ollama_multimodal


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
        self.image_chat_flag = False
        cover = cv2.resize( cv2.imread('assets/MMChat_logo.jpg'), (500,400) )
        self.frame = cover
        self.obd = ObjectDetect(detect_model='yolo11x.pt', seg_model='yolo11x-seg.pt')
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
                            fg='black', bg='white', command=lambda: threading.Thread(target=self.__image_chat__, daemon=True).start())
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
        # 设置显示检测显示器
        self.detect_count_text = tk.Text(self.root, font=('Arial', 8), width=40, height=8)
        self.detect_count_text.place(x=505, y=480)
        self.detect_count_text.insert(tk.END, 'YOLO物体检测数量\n', 'center')
        self.detect_count_text.tag_configure('center', justify='center')
        self.audio_gif_label = tk.Label(self.root, font=('Arial', 8), width=100, height=100,
                            fg='black', bg='white', justify='center', wraplength='200')
        self.audio_gif_label.place_forget()
    def __video_loop__(self):
        while self.video_cap.isOpened():
            ret, frame = self.video_cap.read()
            frame = cv2.flip( cv2.resize( cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (500,400) ), 1)
            if ret: 
                self.frame = frame
                if self.object_detect_flag: 
                    self.frame = self.obd.__detect__(self.frame)
                    self.frame = self.obd.__segmentation__(self.frame)
                    # 更新self.detec_count_text的检测数目的计算
                    # detect_answer_str = [f'{k}:{v}' for k, v in self.obd.__count__().items()]
                    # detect_answer_str = ''.join([f'{x}\n' if (i+1)%2==0 else f'{x}\n' for i,x 
                    #                            in enumerate(detect_answer_str)]).split(',')[0]
                    # 清除前一帧数据
                    self.detect_count_text.delete(1.0, tk.END)
                    self.detect_count_text.insert(tk.END, 'YOLO物体检测数量\n', 'center')
                    self.detect_count_text.tag_configure('center', justify='center')
                    # 插入当前帧数据, 信息分局两侧展示
                    for k,v in self.obd.__count__().items():
                        self.detect_count_text.tag_configure("tab", tabs=(25,))
                        self.detect_count_text.tag_configure('left_red', justify='left', foreground='red')
                        self.detect_count_text.insert(tk.END, f'{k}\t\t\t\t{v}\n', {'left_red','tab'})
                        self.detect_count_text.see(tk.END)
                    # self.detect_count_text.insert(tk.END, detect_answer_str,  'center_red')
                    # self.detect_count_text.tag_configure('center_red', justify='center', foreground='red')
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
        response = ollama_generator(self.prompt)
        self.chat_text.insert(tk.END, '\n'+response, 'left_blue')
        self.chat_text.tag_configure('left_blue', justify='left', foreground='blue')
        self.chat_text.see(tk.END)
        # 实现文字转语音
        with open('data_cached/audio_to_text.txt', 'w', encoding='utf-8') as f:
            f.write(response)
        text_to_audio(audio_text_config())
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
            self.audio_gif_label.place(x=0, y=0)
            self.gifplayer = GifPlayer(self.root, self.audio_gif_label, self.filename,
                                       width=100, height=100)  
            threading.Thread(target=self.__audio_text_conversation__, daemon=True).start()
        else:
            self.gifplayer.__stop__()
            self.audio_gif_label.place_forget()
    def __audio_text_conversation__(self):
        """语音转文字,文字转语音,实现语音聊天"""
        args = audio_text_config()
        # 实现语音转文字
        audio_data = audio_recording(args)
        save_audiodata(audio_data, args)
        self.prompt = audio_to_text(args)
        self.chat_text.insert(tk.END, '\n'+self.prompt, 'right_red')
        self.chat_text.tag_configure('right_red', justify='right', foreground='red')
        self.chat_text.see(tk.END)
        if self.prompt:
            threading.Thread(target=self.__llmchat_response__, daemon=True).start()
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
    def __image_chat__(self):
        """图片聊天功能,获取视频帧图像并直接显示在截屏处"""
        self.image_chat_flag = not self.image_chat_flag
        if self.image_chat_flag and self.video_cap is not None:
            # 截取视频帧
            self.audio_gif_label.place(x=0, y=0)
            self.gifplayer = GifPlayer(self.root, self.audio_gif_label, self.filename,
                                       width=100, height=100)  
            self.screen_shot_frame = cv2.resize( self.frame, (100,100) )
            self.screen_shot_imgtk = ImageTk.PhotoImage(Image.fromarray(self.screen_shot_frame))
            self.over_video_label.config(image=self.screen_shot_imgtk)
            self.over_video_label.image = self.screen_shot_imgtk
            self.over_video_label.place(x=400, y=300)
            # 进行获取用户提示
            args = audio_text_config()
            audio_data = audio_recording(args)
            save_audiodata(audio_data, args)
            self.prompt = audio_to_text(args)
            self.chat_text.insert(tk.END, '\n'+self.prompt, 'right_red')
            self.chat_text.tag_configure('right_red', justify='right', foreground='red')
            self.chat_text.see(tk.END)
            # 进行图像交流
            if self.prompt and self.frame is not None:
                response = ollama_multimodal(
                    frame=self.frame,
                    prompt=self.prompt,
                    temperature=0.9,
                    max_tokens=1000)
                self.chat_text.insert(tk.END, '\n'+response, 'left_blue')
                self.chat_text.tag_configure('left_blue', justify='left', foreground='blue')
            # 实现文字转语音
            with open('data_cached/audio_to_text.txt', 'w', encoding='utf-8') as f:
                f.write(response)
            text_to_audio(audio_text_config())
            self.audio_gif_label.place_forget()
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
