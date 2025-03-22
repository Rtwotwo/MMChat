"""
任务: 导入基础chat小参量模型,配置权重部署configuration,
      实现基本的代码互动沟通与测试。若仍有时间, 可尝试部署
      数据集进行SFT微调监督训练
时间: 2025/03/01-Redal
"""
import os
import sys
import ollama
from openai import OpenAI

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from models.configuration import config


###############################  构建相关的llm_chat函数  ###############################
def get_api_key():
      """use the config function to get the api key"""
      args = config()
      api_path = os.path.join(args.api_dir, args.api_name)
      with open(api_path, 'r', encoding='utf-8') as f:
            api_key = f.read()
      return api_key


def llm_chat(text):
      """use the InternLM API client to generate the response
      :param prompt: the prompt of the user
      :param content: the content of the user"""
      api_key = get_api_key()
      client = OpenAI(base_url="https://internlm-chat.intern-ai.org.cn/puyu/api/v1/",api_key=api_key)
      # describe the prompt to the model
      with open('./api/content.txt', 'r', encoding='utf-8') as f:
            content = f.read()
      prompt = f"""请按照上述的要求回答{content}以下问题：{text}"""

      # Conduct voice interaction testing
      response = client.chat.completions.create(
            model="internlm2.5-latest",
            messages=[{"role": "user", "content": prompt},],
            stream=False)
      chat_text = response.choices[0].message.content
      return chat_text


def ollama_generator(prompt):
      """Use the ollama local llms to generate the response
      :param prompt: the prompt of the user"""
      args = config()
      with open('./api/content.txt', 'r', encoding='utf-8') as f:
            content=f.read()
      prompt = f"""请按照上述的要求回答{content}以下问题：{prompt}"""
      generator = ollama.generate(
            model = args.ollama_key,
            prompt = prompt,
            stream = False,)
      return generator['response']
      


##################################  主控函数测试  ##################################
if __name__ == '__main__':
      text = "解释量子力学?"
      print(llm_chat(text))