import json
import re
import pandas as pd
from collections import defaultdict, Counter

def clean_text(text):
    # Remove special characters from the beginning and end, including spaces, newline characters, asterisks, quotes, and colons.
    return re.sub(r'^[\s\*\n\'\"“”‘’：:]+|[\s\*\n\'\"“”‘’：:]+$', '', text)

import re

# def extract_information(text):
#     # Pattern to match each "Task Category:" and its associated content
#     task_pattern = r"Task Category:\s*(.*?)\n(.*?)(?=(?:\nTask Category:|$))"
#     task_matches = re.findall(task_pattern, text, re.DOTALL)

#     # Initialize result list
#     results = []

#     # Process each task category and corresponding conversation
#     for task_category, task_content in task_matches:
#         # Strip any leading or trailing whitespace
#         task_category = task_category.strip()

#         # Patterns to match instructions and responses for multiple rounds of conversation
#         instruction_pattern = r"<Instruction:\s*(.*?)>(?=\s*<Response:|$)"
#         response_pattern = r"<Response:\s*(.*?)>(?=\s*<Instruction:|$)"

#         # Extract all matches for instructions and responses within the current task content
#         instructions = re.findall(instruction_pattern, task_content, re.DOTALL)
#         responses = re.findall(response_pattern, task_content, re.DOTALL)

#         # Initialize the conversation list
#         conversation = []

#         # Combine instructions and responses in the order they appear
#         if len(instructions) - len(responses) > 1:
#             if responses:
#                 return None
#         pairs = min(len(instructions), len(responses))
#         for i in range(pairs):
#             conversation.append({'from': 'human', 'value': instructions[i].strip()})
#             conversation.append({'from': 'gpt', 'value': responses[i].strip()})

#         # Append the conversation and its task category to the result
#         results.append((conversation, task_category))

#     return results



def process_jsonl(input_path, output_path):
    processed_data = []  # 用于存储处理后的数据
    with open(input_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            data = json.loads(line)
            response = data.get('response', '')
            # 使用正则表达式提取 JSON 数据
            json_data = re.search(r'\{.*\}', response, re.DOTALL)


            if json_data:
                extracted_json = json_data.group()
                try:
                    a = json.loads(extracted_json)
                except:
                    continue
                # print(extracted_json)
            else:
                print("未找到 JSON 数据")
            processed_data.append(a)

            

    # 保存处理后的数据到新的 JSONL 文件
    print (len(processed_data))
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for entry in processed_data:
            outfile.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"处理完成，已保存到 {output_path}")


if __name__ == "__main__":
    # file_name = [
    #     'GEOS(MathV360K)_processed.json',
    #     'GeoQA+(MathV360K)_processed.json',
    #     'Geometry3K(MathV360K)_processed.json',
    #     'IconQA(MathV360K)_processed.json',
    #     'PMC-VQA(MathV360K)_processed.json',
    #     'Super-CLEVR(MathV360K)_processed.json',
    #     'TabMWP(MathV360K)_processed.json',
    #     'UniGeo(MathV360K)_processed.json',
    #     'VizWiz(MathV360K)_processed.json'
    # ]
    # for _ in file_name:
    input_jsonl_file = "/gpfs/public/research/tianyu/COIG-P/role/Qwen2-72B-Instruct_role_card_2140_coig_rewrite_role.jsonl"
    output_jsonl_file = '/gpfs/public/research/tianyu/COIG-P/role/COIG_role.jsonl'
    # output_jsonl_file = input_jsonl_file.replace('math.jsonl', 'math_extract.jsonl')
    process_jsonl(input_jsonl_file, output_jsonl_file)
