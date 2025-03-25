"""
Author: Redal
Date: 2025/03/03
TODO: Create TopRoot Message Information
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import tkinter as tk

class TopMessage(tk.Frame):
    """Temporary Message Information for Getting User's Name"""
    def __init__(self, main_root):
        super().__init__(main_root)
        self.main_root = main_root
        self.__set_widgets__()
        self.top_root = tk.Toplevel(self.main_root)
        self.name = None
    def __set_widgets__(self):
        self.top_root.title('Message Information')
        self.top_root.geometry('400x400')
        self.Button_GetName = tk.Button(self.top_root, text='Get Name', font='Arial',
                        bg='white', fg='black',width=15, height=2, command=self.__GetEntryName__)
        self.Button_GetName.pack()
        self.Entry_GetName = tk.Entry(self.top_root, font='Arial', width=15, justify='center')
        self.Entry_GetName.pack()
    def __GetEntryName__(self):
        self.name = self.Entry_GetName.get()
        self.top_root.destroy()
        return self.name