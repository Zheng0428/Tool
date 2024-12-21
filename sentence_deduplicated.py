import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# 加载预训练的嵌入模型
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# 输入和输出文件路径
input_file = '/gpfs/public/research/tianyu/COIG-P/math/Qwen2-72B-Instruct_NuminaMath-CoT_math_translate_extract.jsonl'
output_file = '/gpfs/public/research/tianyu/COIG-P/math/Qwen2-72B-Instruct_NuminaMath-CoT_math_translate_extract_deduplicated.jsonl'

# 读取jsonl文件并提取problem数据
problems = []
data_entries = []

with open(input_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(tqdm(f, desc="Loading data")):
        data = json.loads(line)
        problem_text = data['problem']
        problems.append(problem_text)
        data_entries.append(data)

# 计算句子嵌入
print("Computing sentence embeddings...")
embeddings = model.encode(problems, convert_to_tensor=True, show_progress_bar=True)
embeddings = embeddings.cpu().numpy()  # 将其转换为numpy数组以便用于FAISS

# 使用FAISS进行去重
index = faiss.IndexFlatL2(embeddings.shape[1])  # 使用L2距离创建索引
faiss.normalize_L2(embeddings)  # FAISS推荐对L2距离的向量进行归一化

index.add(embeddings)  # 将嵌入添加到索引中
_, unique_indices = index.search(embeddings, 1)  # 搜索最近的邻居

# 找到唯一的索引
unique_indices_set = set(unique_indices.flatten())

# 根据唯一索引提取去重后的数据
deduplicated_entries = [data_entries[i] for i in unique_indices_set]

# 将去重后的数据写入新的jsonl文件
with open(output_file, 'w', encoding='utf-8') as f:
    for entry in deduplicated_entries:
        f.write(json.dumps(entry) + '\n')

print(f"去重完成！去重后的数据保存在：{output_file}")
