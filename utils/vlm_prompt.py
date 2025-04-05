"""
Author: Redal
Date: 2025/04/05
TODO: MMChat utils directory vlm_prompt
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import cv2
import ollama 
import tempfile 
from pathlib import Path 
from typing import Union
 

def ollama_multimodal(
    frame: Union[bytes, str],
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1000 ) -> str:
    # 将cv2获取的视频流转成bytes
    if isinstance(frame, bytes):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            f.write(frame) ;img_path = f.name 
    elif isinstance(frame, str):
        img_path = frame
    try:
        response = ollama.generate( 
            model="llava:latest",
            prompt=prompt,
            images=img_path,
            options={"temperature": temperature,
                "num_predict": max_tokens })
        return response["response"]
    except ollama.ResponseError as e:
        print(f"模型调用错误: {e.error}") 
    except FileNotFoundError:
        print(f"图片文件未找到: {img_path}")
 

if __name__ == "__main__":
    # 测试函数
    frame = cv2.imread("assets/face_cls/single_face.jpg")
    _, buffer = cv2.imencode(".jpg", frame)
    result = ollama_multimodal(
        frame=buffer.tobytes(), 
        prompt="分析这张图片中的场景并生成诗歌",
        temperature=0.9 )
    print(result)