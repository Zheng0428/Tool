import json
import math
import os

def split_json_file(input_file, num_parts):
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 计算每个部分的大小
    total_items = len(data)
    items_per_part = math.ceil(total_items / num_parts)
    
    # 获取文件名和扩展名
    file_name, file_extension = os.path.splitext(input_file)
    
    # 切分并保存文件
    for i in range(num_parts):
        start = i * items_per_part
        end = min((i + 1) * items_per_part, total_items)
        part_data = data[start:end]
        
        output_file = f"{file_name}_{i+1}{file_extension}"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(part_data, f, ensure_ascii=False, indent=2)
        
        print(f"已保存: {output_file}")

# 使用示例
input_file = "/gpfs/public/research/tianyu/KOR-Bench/data/captions-1M.json"  # 输入文件名
num_parts = 4  # 要切分的份数

split_json_file(input_file, num_parts)