import os
import requests
import json
import base64

def call_claude_api(prompt, images=None, max_tokens=1000, model="claude-3-7-sonnet-20250219-thinking"):
    """
    使用Python调用Claude API,支持多模态输入
    
    参数:
        prompt (str): 发送给Claude的提示文本
        images (list): 图片文件路径列表
        max_tokens (int): 生成的最大token数量
        model (str): 使用的Claude模型名称
    
    返回:
        dict: API响应的JSON对象
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("请设置ANTHROPIC_API_KEY环境变量")
    
    headers = {
        "Content-Type": "application/json", 
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }

    # 构建消息内容
    content = []
    content.append({"type": "text", "text": prompt})
    
    # 添加图片
    if images:
        for img_path in images:
            with open(img_path, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": img_base64
                    }
                })
    
    data = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": content}
        ]
    }
    
    response = requests.post(
        "https://api.2077ai.org/v1/messages",
        headers=headers,
        json=data
    )
    
    if response.status_code != 200:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")
        
    return response.json()

# 使用示例
if __name__ == "__main__":
    
    prompt = "请描述一下这张图片。"
    images = ["/map-vepfs/tianyu/GPQA/image.png"]  # 图片路径列表
    response = call_claude_api(prompt, images=images)
    
    # 输出Claude的回答
    print(response["content"][0]["text"])