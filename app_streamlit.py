"""
Author: Redal
Date: 2025/03/03
TODO: 构建streamlit模型应用部署网页, 引入VLM的api接口,
      部署网页引用直接开发,实现本地与云端互联
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import streamlit as st
import pandas as pd
import numpy as np


class StreamlitWeb:
      """set the sttreamlit web basical parameters"""
      def __init__(self):
            st.set_page_config(
                  layout='wide', 
                  page_title="Muti-Model Chat",
                  initial_sidebar_state='auto')
            st.header('Welcome to the Muti_Model Chat!')
            
            
