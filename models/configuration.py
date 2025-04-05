"""
Author: Redal
Date: 2025/03/03
TODO: 定义项目所需的参数配置,定义全局参数变量
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
import sys
import argparse
current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)


############################  定义变量解析域配置  #################################
def config():
      parser = argparse.ArgumentParser(description='audio_text_model related arguments definition',
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
      # audio_text_conversion.py related arguments
      parser.add_argument('--model_type', type=str, default='small', 
                        help='openai whisper model type consists of base/small/medium/large')
      parser.add_argument('--uptime_offset', type=int, default=20,
                        help='convert audio to text and the can be recorded up offset time')
      parser.add_argument('--audio_fs', type=int, default=16000,
                        help='audio-to-text and text-to-audio sampling rate')
      parser.add_argument('--audio_channels', type=int, default=1,
                        help='when the audio is recorded, the audio channel')
      parser.add_argument('--silence_duration', type=int, default=2000,
                        help='the silence time should be checked and ms')
      parser.add_argument('--cached_dir', type=str, default=r'./data_cached',
                        help='the directory of cached audio and text data' )
      parser.add_argument('--cached_recorded_audio', type=str, default='recorded_audio.mp3', 
                        help='the name of cached recorded audio data')
      parser.add_argument('--cached_audio_to_text', type=str, default='audio_to_text.txt', 
                        help='the name of cached audio to text data')
      parser.add_argument('--cached_text_to_audio', type=str, default='text_to_audio.mp3', 
                        help='the name of cached text to audio data')
      # llm_chat_model.py related arguments and ollama
      parser.add_argument('--api_dir', type=str, default='./api',
                          help='you can put your api key in the api_dir')
      parser.add_argument('--api_name', type=str, default='internlm_api.txt',
                          help='the name of your api key file internlm/siliconflow api key')
<<<<<<< HEAD
      parser.add_argument('--ollama_key', type=str, default='qwen2.5:1.5b',
=======
      parser.add_argument('--ollama_key', type=str, default='llava:latest',
>>>>>>> 83ab375b1e9c0caafce2a51432e0a20637f44350
                          help='use ollama deepseek-r1:1.5b / qwen2.5:1.5b / internlm2:1.8b / llava:latest')
      args = parser.parse_args()
      return args



############################  主控函数测试  #################################
if __name__ == '__main__':
      args = config()
      for arg in vars(args):
            print(f'{arg}:\t\t{getattr(args, arg)}\t\t')
      