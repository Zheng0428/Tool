import json

def split_jsonl(file_path, output_prefix, chunk_size=300000):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    total_lines = len(lines)
    num_files = (total_lines // chunk_size) + (1 if total_lines % chunk_size != 0 else 0)
    
    for i in range(num_files):
        start = i * chunk_size
        end = start + chunk_size
        chunk_lines = lines[start:end]
        output_file = f"{output_prefix}{i+1}.jsonl"
        
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.writelines(chunk_lines)
        print(f"Created: {output_file} with {len(chunk_lines)} lines")

# 使用该函数来拆分文件
split_jsonl('/gpfs/public/research/tianyu/KOR-Bench/data/NuminaMath-CoT/NuminaMath-CoT.jsonl', '/gpfs/public/research/tianyu/KOR-Bench/data/NuminaMath-CoT/NuminaMath-CoT')
