import tkinter as tk
from PIL import Image, ImageTk
import cv2
import threading
import queue

class LoginInterface(tk.Frame):
    """Create a login interface for user to login"""
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
        self.frame_queue = queue.Queue()
        self.threading = threading.Thread(target=self.__video_loop__)
        self.threading.daemon = True
        self.threading.start()
        # Start the video update loop
        self.after(33, self.__update_video__)

    def __set_widgets__(self):
        self.frame = None
        self.pass_word = None
        self.face_embedding = None
        self.top_root.title('Login Interface')
        self.top_root.geometry('600x600')
        # Set Main title
        self.Button_FaceLogin = tk.Button(self.top_root, text='人脸登陆', font='Arial',
                        bg='white', fg='black', width=15, height=2, command=self.__FaceLogin__)
        self.Button_FaceLogin.place(x=450, y=200)
        self.Button_PasswordLogin = tk.Button(self.top_root, text='密码登陆', font='Arial',
                        bg='white', fg='black', width=15, height=2, command=self.__PasswordLogin__)
        self.Button_PasswordLogin.place(x=450, y=300)
        # Set Main Label for Facial Frames
        self.main_label = tk.Label(self.top_root, justify='center', wraplength=380, width=512, height=512)
        self.main_label.config(text='请选择登入系统的方式\n点击“人脸登入”或“密码登入”即可')
        self.main_label.place(x=0, y=0)

    def __video_loop__(self):
        while self.video_cap.isOpened():
            ret, frame = self.video_cap.read()
            if ret:
                frame = cv2.flip(cv2.cvtColor(cv2.resize(frame, (512, 512)), cv2.COLOR_BGR2RGB), 1)
                self.frame_queue.put(frame)
            else:
                break

    def __update_video__(self):
        try:
            self.frame = self.frame_queue.get_nowait()
            img_tk = ImageTk.PhotoImage(Image.fromarray(self.frame))
            self.main_label.config(image=img_tk)
            self.main_label.image = img_tk
        except queue.Empty:
            pass
        self.after(10, self.__update_video__)

    def __FaceLogin__(self):
        self.face_login = True
        self.top_root.destroy()

    def __PasswordLogin__(self):
        self.password_login = True
        self.top_root.destroy()

if __name__ == "__main__":
    main_root = tk.Tk()
    app = LoginInterface(main_root)
    
    # Run main_root's mainloop in the main thread
    main_root.mainloop()



