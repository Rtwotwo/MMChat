"""
Author: Redal
Date: 2025/03/03
TODO: Create TopRoot Message Information,
      Try design software in a multithreaded manner
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
        self.password = None
        self.__set_widgets__()
        # Wait for the Toplevel window to close
        self.top_root.wait_window()
    def __set_widgets__(self):
        self.top_root.title('Message Information')
        self.top_root.geometry('400x300')
        self.Button_GetName = tk.Button(self.top_root, text='Get Name', font='Arial',
                        bg='white', fg='black',width=15, height=2, command=self.__GetEntryName__)
        self.Button_GetName.pack(pady=20)
        self.Label_GetName = tk.Label(self.top_root, text='Name', font=('Arial',8), justify='left',wraplength=380, width=13, height=2)
        self.Label_GetName.place(x=60, y=105)
        self.Entry_GetName = tk.Entry(self.top_root, font='Arial', width=15, justify='center')
        self.Entry_GetName.pack(pady=20)
        self.Label_Password = tk.Label(self.top_root, text='Password', font=('Arial',8), justify='left',wraplength=380, width=13, height=2)
        self.Label_Password.place(x=60, y=165)
        self.Entry_Password = tk.Entry(self.top_root, font='Arial', width=15, justify='center')
        self.Entry_Password.pack(pady=20)
        self.Label_Info = tk.Label(self.top_root, font='Arial', width=30, height=2)
        self.Label_Info.pack(pady=20)
        self.Label_Info.config(text='Please enter your name and then\nclick the "Get Name" button')
    def __GetEntryName__(self):
        self.name = self.Entry_GetName.get().strip()
        self.password = self.Entry_Password.get().strip()
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
                             '\n  4.Object Detection: Use yolov5 to detect cars and people in the environment' +
                             '\n  5.Spectrogram Histogram: Use spectrogram and histogram about ecah frame ' +
                             '\n  6.Image ToWorld: Use single-picture to reconstruct the world')
        self.Button_Exit = tk.Button(self.top_root, text='Exit', font='Arial', command=self.__exit__)
        self.Button_Exit.pack(pady=20)
    def __exit__(self):
        self.top_root.destroy()
        self.Is_exit = True



if __name__ == '__main__':
    # Test the GetFaceName class
    # root = tk.Tk()
    # root.withdraw()
    # top_message = GetFaceName(root)
    # print("User entered name:", top_message.name)
    # root.mainloop()

    # Test the CreateMessageBox class
    root = tk.Tk()
    root.withdraw()
    mess_box = CreateMessageBox(root)
    root.mainloop()
