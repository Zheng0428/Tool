import pandas as pd
import os,json
from datasets import load_dataset

# def read_parquets(data_path, split='', total_shards=None, shard_idx=None, mapping_key=None):
#     base_path = f'{data_path}/{split}'
#     if os.path.exists(f'{base_path}.parquet'):
#         file_path = f'{base_path}.parquet'
#     else:
#         print (f'{base_path}.parquet')
#         raise FileNotFoundError("No Parquet file found.")
    
#     # 使用 pandas 读取 Parquet 文件
#     data = pd.read_parquet(file_path)
#     if total_shards is not None and shard_idx is not None:  
#         shard_size = len(data) // total_shards
#         start_index = shard_size * shard_idx
#         end_index = start_index + shard_size if shard_idx < total_shards - 1 else len(data)
    
#         if start_index >= len(data):
#             raise IndexError("Shard index exceeds the total number of available shards.")
        
#         shard_data = data.iloc[start_index:end_index]
#     else:
#         shard_data = data
    
#     # 如果传入了 mapping_key，则将数据转换为字典格式，key 为 mapping_key 对应的值
#     if mapping_key:
#         return {row[mapping_key]: row.to_dict() for _, row in shard_data.iterrows() if mapping_key in row}
#     else:
#         return shard_data.to_dict(orient='records')

path = '/gpfs/public/research/tianyu/DAG/dataset/data'
dataset = load_dataset(path, split='train')
output_file = '/gpfs/public/research/tianyu/DAG/dataset/NuminaMath-CoT.jsonl'

with open(output_file, 'w', encoding='utf-8') as f:
    for data in dataset:
        json_str = json.dumps(data, ensure_ascii=False)
        f.write(json_str + '\n')
print(data)