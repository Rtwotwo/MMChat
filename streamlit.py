"""
Author: Redal
Date: 2025/03/03
TODO: 构建streamlit模型应用部署网页, 引入VLM的api接口,
      部署网页引用直接开发,实现本地与云端互联
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import argparse
import streamlit as st
import ollama
st.set_page_config(
        page_title = 'Welcome to MMchat!',
        page_icon = ':robot_face:',
        layout='wide',
        initial_sidebar_state='auto')



##########################  定义变量解析阈  #############################
def streamlit_config():
    parser = argparse.ArgumentParser(description='StreamlitPage related arguments definition',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--main_title', type=str, default='MMChat-Redal', help='The title of the Streamlit web page')
    args = parser.parse_args()
    return args



##########################  MMChatStreamlit页面设计  ####################
class MMChatStreamlit(object):
    """Set the Streamlit web basic parameters"""
    def __init__(self, args, **kwargs):
        self.args = args
        self.__webpage__()

    def __webpage__(self):
        st.title(self.args.main_title)
        # Set the sidebar
        st.sidebar.title('MMchat Settings')
        st.sidebar.header('Choose Model Options')
        st.sidebar.write('Please choose llm model you want to use')
        llm_options = st.sidebar.multiselect('choose models', ['qwen2.5:1.5b', 'internlm2:1.8b', 'deepseek-r1:1.5b'])
        vlm_options = st.sidebar.multiselect('choose vlm models', ['llava:latest', 'llava:7b'])
        # Set the main Page 
        # if st.button('Start Chatting'):

        st.text_input("Please enter your questions for mmchat...")
        st.write(f'You have chosen {llm_options} and {vlm_options}')



##########################  主函数测试分析  #############################
def llm_chat(text):
    """Use the ollama's LLM to chat
    :param text: models' input text"""
    generator = ollama.generate(text)


##########################  主函数测试分析  #############################
if __name__ == '__main__':
    args = streamlit_config()
    mmchat = MMChatStreamlit(args)
    st.write('Hello, Streamlit!') 