"""
Author: Redal
Date: 2025/03/22
TODO: 构建音频-文本互相转换的基础模型,配置调用接口
      使用openai的whisper模型tiny/base/large-v2
Homepage: https://github.com/Rtwotwo/MMchat.git
"""
import os
os.environ["PATH"] += os.pathsep + r'D:\DataAPPs\VS Code\ffmpeg\bin'
import argparse
import whisper
from gtts import gTTS 
import wave 
from playsound import playsound 
import sounddevice as sd
from scipy.io.wavfile import write 
import numpy as np
import webrtcvad 
from llm_chat_model import llm_chat
from llm_chat_model import ollama_generator


############################  定义变量解析域配置  #################################
def audio_text_config():
    parser = argparse.ArgumentParser(description='audio_text_model related arguments definition',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--model_type', type=str, default='small', 
                        help='openai whisper model type consists of base/small/medium/large')
    parser.add_argument('--uptime_offset', type=int, default=5,
                        help='convert audio to text and the can be recorded up offset time')
    parser.add_argument('--audio_fs', type=int, default=16000,
                        help='audio-to-text and text-to-audio sampling rate')
    parser.add_argument('--audio_channels', type=int, default=1,
                        help='when the audio is recorded, the audio channel')
    parser.add_argument('--silence_duration', type=int, default=1000,
                        help='the silence time should be checked and ms')
    parser.add_argument('--cached_dir', type=str, default=r'./data_cached',
                        help='the directory of cached audio and text data' )
    parser.add_argument('--cached_recorded_audio', type=str, default='recorded_audio.mp3', 
                        help='the name of cached recorded audio data')
    parser.add_argument('--cached_audio_to_text', type=str, default='audio_to_text.txt', 
                        help='the name of cached audio to text data')
    parser.add_argument('--cached_text_to_audio', type=str, default='text_to_audio.mp3', 
                        help='the name of cached text to audio data')
    args = parser.parse_args()
    return args



############################  音频录制函数调用接口  ################################
def audio_recording(args):
    """record audio and check the silence time, set a max duration
    :param args.uptime_offset: the audio can be recorded up offset time 
    :param args.silence_duration: the silence time should be checked
    :param args.audio_fs: the audio sampling rate
    :param args.audio_channels: the audio channel"""
    vad = webrtcvad.Vad(0)  
    chunk_duration_ms = 30  
    chunk_size = int(args.audio_fs * chunk_duration_ms / 1000)  
    silence_samples = int(args.audio_fs * args.silence_duration / 1000)
    audio_data = []
    silent_samples_count = 0
    with sd.InputStream(samplerate=args.audio_fs, channels=args.audio_channels, 
                        dtype='int16', blocksize=chunk_size) as stream:
        print(f'====Ready to record audio for {args.uptime_offset} seconds...====')
        total_samples = 0
        while total_samples < args.audio_fs * args.uptime_offset:
            data, _ = stream.read(chunk_size)
            audio_data.append(data)
            # make a surance about silence check and is 16-bit PCM format class
            if not vad.is_speech(data.tobytes(), args.audio_fs): 
                silent_samples_count += chunk_size
            else: silent_samples_count = 0
            
            if silent_samples_count > silence_samples:
                print("====checked the silent audio, end recording early===="); break
            total_samples += chunk_size
    return audio_data
            

def save_audiodata(audio_data, args):
    """save the audio data in the direction ./data_cached/
    :param audio_data: the audio data
    :param args.cached_dir: the directory of cached audio and text data"""
    audio_data = np.concatenate(audio_data, axis=0)
    with wave.open(os.path.join(args.cached_dir, args.cached_recorded_audio), 'wb') as wf:
        # set the audio data format class
        wf.setnchannels(args.audio_channels)
        wf.setsampwidth(2)
        wf.setframerate(args.audio_fs)
        wf.writeframes(audio_data.tobytes())
    print(f'====data has been saved to {os.path.join(args.cached_dir, args.cached_recorded_audio)} ====')
            

def audio_to_text(args):
    """use whisper to convert audio to text
    :param args.cached_dir: the directory of cached audio and text data"""
    audio_to_text_model = whisper.load_model(args.model_type)
    if args is not None:
        translated = audio_to_text_model.transcribe(os.path.join(args.cached_dir,
                     args.cached_recorded_audio), language='zh', temperature=0.2, verbose=True)
    # save the text data to the text file
    with open(os.path.join(args.cached_dir, args.cached_audio_to_text), 
                                'w', encoding='utf-8') as tf:
        tf.write(translated['text'])
    return translated['text']


def text_to_audio(args):
    """use the gtts to convert text to audio
    :param args.cached_dir: the directory of cached audio and text data"""
    audio_to_text_file = os.path.join(args.cached_dir, args.cached_audio_to_text)
    if os.path.exists(audio_to_text_file):
        with open(audio_to_text_file, 'r', encoding='utf-8') as tf:
            text = tf.read()

    if text is not None:
        tts = gTTS(text=text, lang='zh-cn')
        text_to_audio_file = os.path.join(args.cached_dir, args.cached_text_to_audio)
        tts.save(text_to_audio_file)
        # play the text to audio file
        print('====next the text to audio file will be played...====')
        playsound(text_to_audio_file)
    else: raise ValueError('====text is None!====')    

    

#############################  主控制程序函数  #######################################
if __name__ == '__main__':
    # TODO analyse the relationship between the 
    # interaction input audio and output text
    args = audio_text_config()
    audio_data = audio_recording(args)
    save_audiodata(audio_data, args)
    text = audio_to_text(args)
    print(f'====The text is: {text}====')

    response_text = ollama_generator(text)
    with open('data_cached/audio_to_text.txt', 'w', encoding='utf-8') as f:
        f.write(response_text)
    text_to_audio(args)