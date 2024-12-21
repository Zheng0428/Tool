import json
import random

def sample_json(input_file, sample_size=1000):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sampled_data = random.sample(data, min(sample_size, len(data)))
    
    output_file = input_file.replace(".json", "_sample.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sampled_data, f, ensure_ascii=False, indent=4)

def sample_jsonl(input_file, sample_size=1000):
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    
    sampled_data = random.sample(data, min(sample_size, len(data)))
    
    output_file = input_file.replace(".jsonl", "_sample.jsonl")
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in sampled_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

# Example usage
# sample_json('/gpfs/public/research/jiawei/visual_web_inst/embedding_ori.json')
# sample_json('/gpfs/public/research/jiawei/visual_web_inst/embedding_re.json')
sample_jsonl('/gpfs/public/research/tianyu/DAG/dataset/NuminaMath/chains_sample.jsonl', 100)
