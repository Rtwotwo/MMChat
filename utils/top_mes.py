"""
Author: Redal
Date: 2025/03/03
TODO: Create TopRoot Message Information
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import tkinter as tk


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


if __name__ == '__main__':
    # Test the GetFaceName class
    root = tk.Tk()
    root.withdraw()
    top_message = GetFaceName(root)
    print("User entered name:", top_message.name)
    root.mainloop()