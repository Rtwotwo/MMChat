import os
import cv2
import threading
import queue
import tkinter as tk
from PIL import Image, ImageTk
from models.llm_chat_model import ollama_generator
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
        self.queue = queue.Queue()
        self.image_tk = None
        self.image_hist_tk = None
        self.image_freq_tk = None
        self.video_thread = threading.Thread(target=self.__video_loop__)
        self.video_thread.daemon = True
        self.video_thread.start()
        
        self.model_interaction_thread = threading.Thread(target=self.__model_interaction_loop__)
        self.model_interaction_thread.daemon = True
        self.model_interaction_thread.start()

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
        self.chat_text = tk.Text(self.root, font=('Arial', 8), bg='white', width=40, height=27)
        self.chat_text.place(x=505, y=0)
        self.chat_text.insert(tk.END,'欢迎使用MMChat-ModelChatApp\n', 'center')
        self.chat_text.tag_configure('center', justify='center')
        self.entry_mess = tk.Entry(self.root, font=('Arial', 8), width=30)
        self.entry_mess.place(x=505, y=384)
        self.sendchat_button = tk.Button(self.root, text='发送', font=('Arial', 8), width=10, height=1,
                            fg='black', bg='white', command=self.__send_chat__)
        self.sendchat_button.place(x=680, y=384)
    def __video_loop__(self):
        while self.video_cap.isOpened():
            ret, frame = self.video_cap.read()
            if not ret: break
            frame = cv2.flip(cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (500,400)), 1)
            self.frame = frame
            self.__update_video__()

    def __update_video__(self):
        image = Image.fromarray(self.frame)
        image_hist = Image.fromarray(ComputeHistogramImage(self.frame))
        image_freq = Image.fromarray(CalculateSpectrogramImage(self.frame))

        if self.image_tk is None:
            self.image_tk = ImageTk.PhotoImage(image)
            self.image_hist_tk = ImageTk.PhotoImage(image_hist)
            self.image_freq_tk = ImageTk.PhotoImage(image_freq)
        else:
            self.image_tk.paste(image)
            self.image_hist_tk.paste(image_hist)
            self.image_freq_tk.paste(image_freq)

        self.video_label.config(image=self.image_tk)
        self.histogram_label.config(image=self.image_hist_tk)
        self.spectrogram_label.config(image=self.image_freq_tk)
        self.after(10, self.__update_video__)

    def __model_interaction_loop__(self):
        while True:
            if not self.queue.empty():
                message = self.queue.get()
                self.process_message(message)

    def process_message(self, message):
        response = ollama_generator(message)
        self.chat_text.insert(tk.END, '\n' + response, 'left')
        self.chat_text.tag_configure('left', justify='left')
        self.chat_text.see(tk.END)

    def __send_chat__(self):
        """用户发送聊天信息给聊天框,信息居右"""
        user_input = self.entry_mess.get().strip()
        if user_input:
            self.chat_text.insert(tk.END, '\n'+user_input, 'right')
            self.chat_text.tag_configure('right', justify='right')
            self.entry_mess.delete(0, tk.END)
            self.chat_text.see(tk.END)
            self.queue.put(user_input)


if __name__ == '__main__':
    root = tk.Tk()
    app = ModelChatApp(root)
    app.mainloop()