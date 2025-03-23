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
from models.face_cls_model import FaceRecognition, face_config
st.set_page_config(
        layout='wide',
        page_title='MMChat-Redal',
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
        st.header('Welcome to MMChat!')



##########################  主函数测试分析  #############################
if __name__ == '__main__':
    args = streamlit_config()
    mmchat = MMChatStreamlit(args)
    st.write('Hello, Streamlit!') 