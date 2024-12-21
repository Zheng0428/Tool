#!/usr/bin/env python
# coding: utf-8

import asyncio
import configparser
from litellm import Router
from litellm.types.utils import ModelResponse

# 加载配置文件中的API密钥
API_KEY = "273b83a4084f4c5b8d2f53aaf99ae0d3"

# 创建Router实例
model_list = [
    {
        "model_name": "moyi-chat-v03-sglang",  # 使用的模型名称
        "litellm_params": {
            "model": "openai/moyi-chat-v03-sglang",  # 实际模型名称
            "api_key": API_KEY,
            "api_base": "http://xcs-moyi-chat-v03-sglang-2lntt.prod.svc.cluster.local:30000/v1",  # API 基地址
        }
    }
]

client = Router(model_list=model_list)

# 测试函数，提交请求
async def test_api():
    request_data = {
        "model": "moyi-chat-v03-sglang",
        "messages": [{"role": "user", "content": "Hello! Can you explain what AI is?"}],
        "extra_body": {
            "max_tokens": 50,
            "temperature": 0.7,
            "top_p": 0.9,
        },
    }
    response = await client.acompletion(**request_data)
    return response

# 异步运行测试
async def main():
    response = await test_api()
    print(response)

# 运行异步函数
if __name__ == "__main__":
    asyncio.run(main())
