"""
Author: Redal
Date: 2025/03/03
TODO: 系统函数框架设计,手动选择输入功能
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import json
import sys
import cv2
import torch
import argparse
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from models.face_cls_model import FaceRecognition, face_config
from utils.face_cls import FaceVisiblity, DeciderCenter
from utils.top_mes import GetFaceName, CreateMessageBox
from facenet_pytorch import MTCNN
from app_authorization import LoginInterface
from app_sysfunc import Gesture_Style_APP

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')



########################  配置tkinter的界面配置  ###########################
def Tkinter_Config():
      """The GUI is defined for tkinter configuration"""
      parser = argparse.ArgumentParser(description='MMChat GUI configuration',
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
      parser.add_argument_group('GUI Main Window Settings')
      parser.add_argument('--gui_title', type=str, default='MMChat', help='The title of the GUI window')
      parser.add_argument('--gui_width', type=str, default='800', help='The width of the GUI window')
      parser.add_argument('--gui_height', type=str, default='512', help='The height of the GUI window')
      parser.add_argument('--coverimg_path', type=str, default='assets/MMChat_app.jpg', help='The audio shower of the GUI window')
      parser.add_argument_group('Facial Authoriation Settings')
      parser.add_argument('--face_emb_savepath', type=str, default='./data_cached/', help='Save Facial Embedding SavePath')
      parser.add_argument('--face_emb_jsonname', type=str, default='face_emb.json', help='Save Facial Embedding JsonName')
      parser.add_argument('--password_emb_savepath', type=str, default='./data_cached/', help='Save Password Embedding SavePath')
      parser.add_argument('--password_emb_jsonname', type=str, default='password_emb.json', help='Save Password Embedding JsonName')
      args = parser.parse_args()
      return args



########################  构造基本GUI界面框架  ###########################
class MMChatTkinter(tk.Frame):
      """The GUI is designed to interact with multi_models tkinter"""
      def __init__(self, root, args):
            super().__init__(root)
            self.root = root
            self.args = args
            self.__set_flags__()
            self.__set_params__()
            self.__widgets__()
            # Initialize video capture and threading
            self.camera_lock = threading.Lock()
            # Initialize functions 
            self.FaceRe = FaceRecognition(face_config())
            self.mtcnn = MTCNN(image_size=512, margin=0, keep_all=False, post_process=True)
      def __set_flags__(self):
            self.main_window_show = False
            self.face_authentication_flag = False
            self.button_interaction_flag = False
            self.button_funcrelated_flag = False
            self.button_systemfunc_flag = False
      def __set_params__(self):
            self.facial_info = {}
            self.password_info = {}
            self.name = None
      def __widgets__(self):
            self.root.title('MMChat-Redal')
            self.root.geometry(f'{self.args.gui_width}x{self.args.gui_height}')
            self.root.configure(bg='white')
            self.main_label = tk.Label(self.root,width=512, height=512); self.main_label.place(x=0, y=0)
            # Set the background image for main label
            img_tk = ImageTk.PhotoImage(Image.open(self.args.coverimg_path).resize((512,512)))
            self.main_label.config(image=img_tk)
            self.main_label.image = img_tk
            # Set MMChat App Introduction label
            self.introduction_label = tk.Label(self.root, font='Arial',bg='white', width=25, height=5)
            self.introduction_label.place(x=550, y=0)
            self.introduction_label.config(text='MMChat App Introduction')
            # Functional Button Related MMchat mode
            self.button_authentication = tk.Button(self.root, text='用户注册', font=('Arial',8),
                        bg='white', fg='black',width=10, height=2, command=self.__button_authentication__)
            self.button_authentication.place(x=580, y=300)
            self.button_interaction = tk.Button(self.root, text='身份验证', font=('Arial',8),
                        bg='white', fg='black',width=10, height=2, command=self.__button_interaction__)
            self.button_interaction.place(x=680, y=300)
            self.button_funcrelated = tk.Button(self.root, text='功能关于', font=('Arial',8),
                        bg='white', fg='black', width=10, height=2, command=self.__button_funcrelated__) 
            self.button_funcrelated.place(x=580, y=340)
            self.button_systemfunc = tk.Button(self.root, text='系统功能', font=('Arial',8),
                        bg='white', fg='black', width=10, height=2, command=self.__button_systemfunc__)
            self.button_systemfunc.place(x=680, y=340)
            self.button_exitsystem = tk.Button(self.root, text='退出系统', font=('Arial',8),
                        bg='white', fg='black', width=10, height=2, command=self.__button_exitsystem__) 
            self.button_exitsystem.place(x=580, y=380)
            # Set the main app's information
            self.Label_info = tk.Label(self.root, font=('Arial',8),bg='white', width=40, height=10)
            self.Label_info.place(x=540, y=100)
            self.Label_info.config(text='Welcome to MMChat App' + 
                                   '\n1.MMChat是一款用于人机交互的软件系统,\n集成了一系列的多模态交互功能'+ 
                                   '\n2.软件主要包括手势识别控制、语音控制、\n模型交互、环境感知等一系列功能' + 
                                   '\n3.用户首先需要注册信息才可进入系统')
      def __video_loop__(self):
            while self.video_cap.isOpened():
                  with self.camera_lock:
                        ret, frame = self.video_cap.read()
                  self.frame = cv2.flip( cv2.resize(cv2.cvtColor(frame, 
                        cv2.COLOR_BGR2RGB), (512, 512)), 1 )
                  if ret: 
                        """Program main execution logic"""
                        if self.face_authentication_flag: 
                              # Plot the circle aera for embedding
                              cv2.circle(self.frame, (256,256), 200, (0, 0, 255), 2)
                              cv2.circle(self.frame, (256,256), 100, (0, 0, 255), 2)
                              try:
                                    if DeciderCenter(self.mtcnn, frame):
                                          # Facial Recognition 
                                          face_emb_path = os.path.join(self.args.face_emb_savepath, self.args.face_emb_jsonname)
                                          password_emb_path = os.path.join(self.args.password_emb_savepath, self.args.password_emb_jsonname)
                                          # Extract facial embedding and save it into json file
                                          _, face_embedding = self.FaceRe.__extract__(frame, all_faces=False)
                                          topmessage = GetFaceName(self.root)
                                          # warning: the face embeding cosists list[array[]]
                                          self.facial_info[topmessage.name] = face_embedding[0].tolist()
                                          self.password_info[topmessage.name] = topmessage.password
                                          if topmessage.name and topmessage.password is not None:
                                                with open(face_emb_path, 'w+',encoding='utf-8') as jf:
                                                      self.facial_info = dict(filter(lambda item: item[0] is not None, self.facial_info.items()))
                                                      jf.write(json.dumps(self.facial_info, ensure_ascii=False, indent=4))
                                                with open(password_emb_path, 'w+',encoding='utf-8') as jf:
                                                      self.password_info = dict(filter(lambda item: item[0] is not None, self.password_info.items()))
                                                      jf.write(json.dumps(self.password_info, ensure_ascii=False, indent=4))
                                          # Close Facial Authentication windows 
                                          self.face_authentication_flag = not self.face_authentication_flag
                                          self.main_window_show = not self.main_window_show
                                          self.video_cap.release()
                                    self.frame = FaceVisiblity(self.mtcnn, self.frame)
                              except: pass
                              self.__video_show__()
                        else: # No functions activated
                              self.__video_show__() 
                  else: break
      def __video_show__(self):
            if self.main_window_show: 
                  img_tk = ImageTk.PhotoImage(Image.fromarray(self.frame))
            else: img_tk = ImageTk.PhotoImage(Image.open(self.args.coverimg_path).resize((512,512)))
            self.main_label.config(image=img_tk)
            self.main_label.image = img_tk
            self.after(10)
      def __button_authentication__(self):
            self.main_window_show = not self.main_window_show
            self.face_authentication_flag = not self.face_authentication_flag
            if self.main_window_show: 
                  self.video_cap = cv2.VideoCapture(0)
                  self.threading = threading.Thread(target=self.__video_loop__)
                  self.threading.daemon = True
                  self.threading.start()
            else: 
                  self.main_window_show = not self.main_window_show
                  img_tk = ImageTk.PhotoImage(Image.open(self.args.coverimg_path).resize((512,512)))
                  self.main_label.config(image=img_tk)
                  self.main_label.image = img_tk
      def __button_interaction__(self):
            self.button_interaction_flag = not self.button_interaction_flag
            login_window = tk.Toplevel(self.root)
            login_interface = LoginInterface(login_window)
      def __button_funcrelated__(self):
            self.button_funcrelated_flag = not self.button_funcrelated_flag
            message_box = CreateMessageBox(self.root)
            if message_box.Is_exit: 
                  self.button_funcrelated_flag = not self.button_funcrelated_flag
      def __button_systemfunc__(self):
            self.button_systemfunc_flag = not self.button_systemfunc_flag
            system_root = tk.Toplevel(self.root)
            system_interface = Gesture_Style_APP(system_root)
      def __button_exitsystem__(self):
            self.root.quit()

            

########################  主函数测试分析  ###########################
if __name__ == '__main__':
      args = Tkinter_Config()
      root = tk.Tk()
      app = MMChatTkinter(root, args)
      app.mainloop()