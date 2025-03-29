"""
Author: Redal
Date: 2025/03/03
TODO: Create TopRoot Message Information
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import cv2
import tkinter as tk
import threading
import queue
from PIL import Image, ImageTk


class GetFaceName(tk.Frame):
    """Temporary Message Information for Getting User's Name
    :param return: self.name is the needy name"""
    def __init__(self, main_root):
        super().__init__(main_root)
        self.main_root = main_root
        self.top_root = tk.Toplevel(self.main_root)
        # Set the Related window settings
        self.name = None
        self.__set_widgets__()
        # Wait for the Toplevel window to close
        self.top_root.wait_window()
    def __set_widgets__(self):
        self.top_root.title('Message Information')
        self.top_root.geometry('400x300')
        self.Button_GetName = tk.Button(self.top_root, text='Get Name', font='Arial',
                        bg='white', fg='black',width=15, height=2, command=self.__GetEntryName__)
        self.Button_GetName.pack(pady=20)
        self.Entry_GetName = tk.Entry(self.top_root, font='Arial', width=15, justify='center')
        self.Entry_GetName.pack(pady=20)
        self.Label_Info = tk.Label(self.top_root, font='Arial', width=30, height=2)
        self.Label_Info.pack(pady=20)
        self.Label_Info.config(text='Please enter your name and then\nclick the "Get Name" button')
    def __GetEntryName__(self):
        self.name = self.Entry_GetName.get().strip()
        if not self.name:
            self.Label_Info.config(text='Cannot get name of NoneType')
        else: self.top_root.destroy()


class CreateMessageBox(tk.Frame):
    """Create a message box for introducing the system basic functions"""
    def __init__(self, main_root):
        super().__init__(main_root)
        self.main_root = main_root
        self.Is_exit = False
        self.top_root = tk.Toplevel(self.main_root)
        # Set the Related window settings
        self.__set_widgets__()
        # Wait for the Toplevel window to close
        self.top_root.wait_window()
    def __set_widgets__(self):
        self.top_root.title('Message Information')
        self.top_root.geometry('400x300')
        # Set Main title
        self.Label_title = tk.Label(self.top_root, font=('Arial, 8'), justify='center', wraplength=380, width=60, height=1)
        self.Label_title.pack(pady=20); self.Label_title.config(text="MMChat System Functions' Information" )
        # Set System Functions' Information
        self.Label_Info = tk.Label(self.top_root, font=('Arial',8), justify='left',wraplength=380, width=65, height=6)
        self.Label_Info.pack(pady=20)
        self.Label_Info.config(text='\n  1.Gesture Control: Use your hand to control the posture of uav' + 
                             '\n  2.Face Autherization: According to facial information to open system' + 
                             '\n  3.Multimodal Interaction: Interact with V/LLM model for better experience' + 
                             '\n  4.Object Detection: Use yolov5 to detect cars and people in curent environment' +
                             '\n  5.Spectrogram Histogram: Use spectrogram and histogram about ecah frame ' +
                             '\n  6.Image ToWorld: Use single-picture to reconstruct the world')
        self.Button_Exit = tk.Button(self.top_root, text='Exit', font='Arial', command=self.__exit__)
        self.Button_Exit.pack(pady=20)
    def __exit__(self):
        self.top_root.destroy()
        self.Is_exit = True


class LoginInterface(tk.Frame):
    """Create a lgoin interface for user to login"""
    def __init__(self, main_root):
        super().__init__(main_root)
        self.main_root = main_root
        self.face_login = False
        self.password_login = False
        self.main_window_show = False
        self.top_root = tk.Toplevel(self.main_root)
        # Set the Related window settings
        self.__set_widgets__()
        # Setting the video_cap
        self.video_cap = cv2.VideoCapture(0)
        self.threading = threading.Thread(target=self.__video_loop__)
        self.threading.daemon = True
        self.threading.start()
        # Wait for the Toplevel window to close
        self.top_root.wait_window()
    def __set_widgets__(self):
        self.frame = None
        self.pass_word = None
        self.face_embedding = None
        self.top_root.title('Login Interface')
        self.top_root.geometry('600x600')
        # Set Main title
        self.Button_FaceLogin = tk.Button(self.top_root, text='人脸登陆', font='Arial',
                        bg='white', fg='black',width=15, height=2, command=self.__FaceLogin__)
        self.Button_FaceLogin.place(x = 540, y=200)
        self.Button_PasswordLogin = tk.Button(self.top_root, text='密码登陆', font='Arial',
                        bg='white', fg='black',width=15, height=2, command=self.__PasswordLogin__)
        self.Button_PasswordLogin.place(x = 600, y=200)
        # Set Mian Label for Facial Frames
        self.main_label = tk.Label(self.top_root, justify='center', wraplength=380, width=512, height=512)
        self.main_label.config(text='请选择登入系统的方式\n点击“人脸登入”或“密码登入”即可')
        self.main_label.place(x=0, y=0)
    def __video_loop__(self):
        while self.video_cap.isOpened():
            ret, frame = self.video_cap.read()
            frame = cv2.flip( cv2.cvtColor( cv2.resize(frame, (512, 512)), cv2.COLOR_BGR2RGB ), 1 )
            if ret:
                self.frame = frame
                self.__video_show__()
            else: break
    def __video_show__(self):
            if self.main_window_show: 
                self.main_label.config(text='请选择登入系统的方式\n点击“人脸登入”或“密码登入”即可')
            else: 
                img_tk = ImageTk.PhotoImage(Image.fromarray(self.frame))
                self.main_label.config(image=img_tk)
                self.main_label.image = img_tk
                self.after(33)
    def __FaceLogin__(self):
        self.face_login = True
        self.top_root.destroy()
    def __PasswordLogin__(self):
        self.password_login = True
        self.top_root.destroy()



if __name__ == '__main__':
    # Test the GetFaceName class
    # root = tk.Tk()
    # root.withdraw()
    # top_message = GetFaceName(root)
    # print("User entered name:", top_message.name)
    # root.mainloop()

    # Test the CreateMessageBox class
    # root = tk.Tk()
    # root.withdraw()
    # mess_box = CreateMessageBox(root)
    # root.mainloop()

    # Test the LoginInterface class
    root = tk.Tk()
    root.withdraw()
    login_interface = LoginInterface(root)
    root.mainloop()
    