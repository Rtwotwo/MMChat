import ollama 
prompt = "请解释一下量子纠缠现象" 

generator = ollama.generate(  
    model="internlm2:1.8b", 
    prompt=prompt, 
    stream=True ) 

try: 
    for part in generator: 
        # 打印每个流式响应的部分 
        print(part["response"], end="", flush=True) 
except KeyboardInterrupt: 
    print("\n生成过程被手动中断。") 
except Exception as e: 
    print(f"发生错误: {e}") 
 