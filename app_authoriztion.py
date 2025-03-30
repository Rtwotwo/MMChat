"""
Author: Redal
Date: 2025/03/30
TODO: 设计身份校验系统, 以获取进入系统的资格
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import json
import cv2
import tkinter as tk
import threading
import queue
import numpy as np
from PIL import Image, ImageTk
from facenet_pytorch import MTCNN
from utils.face_cls import FaceVisiblity, DeciderCenter
from models.face_cls_model import FaceRecognition, face_config


class LoginInterface(tk.Frame):
    """Create a lgoin interface for user to login"""
    def __init__(self, main_root):
        super().__init__(main_root)
        self.main_root = main_root
        self.running = True
        self.face_login = False
        self.password_login = False
        self.main_window_show = False
        self.top_root = tk.Toplevel(self.main_root)
        # Set the Related window settings
        self.__set_widgets__()
        self.FaceRe = FaceRecognition(face_config())
        self.mtcnn = MTCNN(image_size=512, margin=0, keep_all=False, post_process=True)
        # Setting the video_cap
        self.video_cap = cv2.VideoCapture(0)
        self.frame_queue = queue.Queue()
        self.threading = threading.Thread(target=self.__video_loop__)
        self.threading.daemon = True
        self.threading.start()
        self.after(10, self.__update_video__)
        # Wait for the Toplevel window to close
        # Warning: open the function could block main thread
        # self.top_root.wait_window()
        self.top_root.protocol("WM_DELETE_WINDOW", self.__Return__)
    def __set_widgets__(self):
        self.frame = None
        self.name = 'UnKnown'
        self.pass_word = None
        self.face_embedding = None
        self.top_root.title('Login Interface')
        self.top_root.geometry('650x512')
        # Set Main title
        self.Button_FaceLogin = tk.Button(self.top_root, text='人脸登陆', font='Arial',
                        bg='white', fg='black',width=10, height=1, command=self.__FaceLogin__)
        self.Button_FaceLogin.place(x = 540, y=200)
        self.Button_PasswordLogin = tk.Button(self.top_root, text='密码登陆', font='Arial',
                        bg='white', fg='black',width=10, height=1, command=self.__PasswordLogin__)
        self.Button_PasswordLogin.place(x = 540, y=250)
        self.Button_Return = tk.Button(self.top_root, text='返回主界面', font='Arial',
                        bg='white', fg='black',width=10, height=1, command=self.__Return__)
        self.Button_Return.place(x = 540, y=300)
        # Set Mian Label for Facial Frames
        self.Entry_GetPassWord = tk.Entry(self.top_root, font=('Arial', 12), width=10, show='*', bg='white', fg='black')
        self.Entry_GetPassWord.place(x=540, y=60)
        self.Button_GetPassWord = tk.Button(self.top_root, text='填写密码', font='Arial',
                        bg='white', fg='black',width=10, height=1, command=self.__GetPassWord__)
        self.Button_GetPassWord.place(x=540, y=80)
        self.main_label = tk.Label(self.top_root, justify='center', wraplength=380, width=512, height=512)
        self.main_label.config(text='请选择登入系统的方式\n点击“人脸登入”或“密码登入”即可')
        self.main_label.place(x=0, y=0)
        # Show the Name recognized
        self.name_label = tk.Label(self.top_root, justify='center', font='Arial',wraplength=380, width=15, height=1)
        self.name_label.config(text='姓名: ' + self.name); self.name_label.place(x=520, y=10)
    def __video_loop__(self):
        while self.running and self.video_cap.isOpened():
            with self.main_root.camera_lock:  # 共享主界面的资源锁
                if not self.video_cap.isOpened():break
                ret, frame = self.video_cap.read()
            frame = cv2.flip( cv2.cvtColor( cv2.resize(frame, (512, 512)), cv2.COLOR_BGR2RGB ), 1 )
            # if succeed, destroy the login interface
            if ret:
                if self.face_login:
                    # Use for Facial Authorization
                    self.frame = frame
                    if DeciderCenter(self.mtcnn, self.frame):
                        # Extract facial embedding and save it into json file
                        _, self.face_embedding = self.FaceRe.__extract__(frame, all_faces=False)
                        if self.face_embedding:
                            self.face_embedding = self.face_embedding[0].tolist()
                            # Read databse facial embedding from json file
                            with open('./data_cached/face_emb.json', 'r') as f:
                                database_emb = json.load(f)
                            # Calculate the distance between query embedding and database embedding
                            min_distance = float('inf')
                            for name, embedding in database_emb.items():
                                distance = np.linalg.norm(np.array(self.face_embedding) - np.array(embedding))
                                if distance < min_distance:
                                    min_distance = distance
                                    self.name = name
                            print(min_distance)
                            # Set threshold=0.45 to exclude strangers
                            threshold = 0.45
                            if min_distance > threshold:
                                self.name = 'Unknown'
                            # Once the face is recognized, stop the loop
                            if self.name != 'Unknown': self.face_login = not self.face_login
                        else: self.name = 'UnKnown'
                    self.frame_queue.put(frame)

                elif self.password_login:
                    # Use for Password Authorization
                    self.main_label.config(text='请输入密码')
                else:
                    if self.name != 'Unknown':
                        self.name_label.config(text='姓名: ' + self.name)
                    self.frame = frame
                    self.frame_queue.put(self.frame)
            else: break
    def __update_video__(self):
        try:
            frame = self.frame_queue.get_nowait()
            if self.face_login:
                frame = FaceVisiblity(self.mtcnn, self.frame)
                cv2.circle(frame, (256, 256), 200, (0, 0, 255), 2)
                cv2.putText(frame, self.name, (256, 256), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            img_tk = ImageTk.PhotoImage(Image.fromarray(frame))
            self.main_label.config(image=img_tk)
            self.main_label.image = img_tk
        except queue.Empty: pass
        self.after(10, self.__update_video__)
    def __GetPassWord__(self):
        self.pass_word = self.Entry_GetPassWord.get()
        with open('./data_cached/password_emb.json', 'r') as f:
            database_emb = json.load(f)
        database_emb = {p: name for name, p in database_emb.items()}
        if self.pass_word in database_emb.keys():
            self.name = database_emb[self.pass_word]
            self.password_login = not self.password_login
            self.name_label.config(text=f'姓名: {self.name}')
    def __FaceLogin__(self):
        self.face_login = not self.face_login
    def __PasswordLogin__(self):
        self.password_login = not self.password_login
    def __Return__(self):
        self.running = False
        if self.threading.is_alive():
            # Wait for the thread to end
            self.threading.join(timeout=1) 
        self.video_cap.release()
        self.top_root.destroy()


if __name__ == '__main__':
    # Test the LoginInterface class
    root = tk.Tk()
    root.withdraw()
    login_interface = LoginInterface(root)
    root.mainloop()