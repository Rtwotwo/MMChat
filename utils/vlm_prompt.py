"""
Author: Redal
Date: 2025/04/05
TODO: MMChat utils directory vlm_prompt
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import cv2
import ollama 
import base64
import tempfile 
from pathlib import Path 
from typing import Union
 


def ollama_multimodal(
    frame: Union[bytes, str],
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1000 ) -> str:
    """llava:,latest进行多模态处理, 直接处理输入的图像帧数据
    :param frame: cv2.capture()采集二点摄像头数据
    :param prompt: 模型数据的输入prompt"""
    # 将图像转换为 Base64 字符串 
    _, img_encoded = cv2.imencode('.jpg',  frame)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
    with open('./api/content.txt', 'r', encoding='utf-8') as f:
            content = f.read()
    prompt = f"""请按照上述的要求回答{content}以下问题：{prompt}"""
    response = ollama.generate( 
        model="llava:latest",
        prompt=prompt,
        images=[img_base64],  # 传递 Base64 字符串列表 
        options={"temperature": temperature,
                 "num_predict": max_tokens })
    return response["response"]


if __name__ == "__main__":
    # 测试函数
    frame = cv2.imread("assets/face_cls/single_face.jpg")
    result = ollama_multimodal(
        frame=frame, 
        prompt="分析这张图片中的场景并生成诗歌",
        temperature=0.9 )
    print(result)