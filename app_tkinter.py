"""
Author: Redal
Date: 2025/03/03
TODO: 多模态语音、视觉、手势模型的搭建, 并且构建tkinter的GUI界面框架
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import sys
import cv2
import torch
import argparse
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from models.face_cls_model import FaceRecognition, face_config
from utils.face_cls import face_visiblity

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')



########################  配置tkinter的界面配置  ###########################
def Tkinter_Config():
      """The GUI is defined for tkinter configuration"""
      parser = argparse.ArgumentParser(description='MMChat GUI configuration',
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
      parser.add_argument_group('GUI Main Window Settings')
      parser.add_argument('--gui_title', type=str, default='MMChat', help='The title of the GUI window')
      parser.add_argument('--gui_width', type=str, default='800', help='The width of the GUI window')
      parser.add_argument('--gui_height', type=str, default='600', help='The height of the GUI window')
      parser.add_argument('--coverimg_path', type=str, default='assets/MMChat_app.jpg', help='The audio shower of the GUI window')
      parser.add_argument_group('Facial Authoriation Settings')
      parser.add_argument('--face_emb_savepath', type=str, default='./data_cached/', help='Save Facial Embedding SavePath')
      parser.add_argument('--face_emb_jsonname', type=str, default='face_emb.json', help='Save Facial Embedding JsonName')
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
            self.__widgets__()
            # Initialize video capture and threading
            self.video_cap = cv2.VideoCapture(0)
            self.threading = threading.Thread(target=self.__video_loop__)
            self.threading.daemon = True
            self.threading.start()
            # Initialize functions 
            self.FaceRe = FaceRecognition(face_config())
      def __set_flags__(self):
            self.main_window_show = False
            self.face_authentication_flag = False
            self.audio_llmchat_flag = False
            self.environment_vlm_flag = False
            self.gesture_control_flag = False
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
            self.button_authentication = tk.Button(self.root, text='Face Authentication', font='Arial',
                        bg='white', fg='black',width=15, height=2, command=self.__button_authentication__)
            self.button_authentication.place(x=520, y=100)

      def __video_loop__(self):
            while self.video_cap.isOpened():
                  ret, frame = self.video_cap.read()
                  self.frame = cv2.flip( cv2.resize(cv2.cvtColor(frame, 
                        cv2.COLOR_BGR2RGB), (512, 512)), 1 )
                  if ret: 
                        """Program main execution logic"""
                        if self.face_authentication_flag: 
                              # Facial Recognition 
                              face_emb_path = os.path.join(self.args.face_emb_savepath, 
                                                           self.args.face_emb_jsonpath)
                              with open(face_emb_path, 'w+') as jf:
                                    # Extract facial embedding and save it into json file
                                    facial_info = {}
                                    face_embedding = self.FaceRe.__extract__(self.frame)
                                    facial_info['Name'] = 'Redal' # TODO
                                    facial_info['Embedding'] = face_embedding
                              self.frame = face_visiblity(self.frame)
                              self.__video_show__()

                        elif self.gesture_control_flag: 
                              # Gesture Control Multimodal
                              pass

                        else: # No functions activated
                              self.__video_show__() 
                  else: break
      def __video_show__(self):
            if self.main_window_show: 
                  img_tk = ImageTk.PhotoImage(Image.fromarray(self.frame))
            else: img_tk = ImageTk.PhotoImage(Image.open(self.args.coverimg_path).resize((512,512)))
            self.main_label.config(image=img_tk)
            self.main_label.image = img_tk
            self.after(33)
      def __button_authentication__(self):
            self.main_window_show = not self.main_window_show
            self.face_authentication_flag = not self.face_authentication_flag

            

########################  主函数测试分析  ###########################
if __name__ == '__main__':
      args = Tkinter_Config()
      root = tk.Tk()
      app = MMChatTkinter(root, args)
      app.mainloop()
            