import json
from datasets import load_dataset

def read_hf(data_path, split='train', mapping_key=None):
    # Load the specified Hugging Face dataset and split
    ds = load_dataset(data_path, split=split)

    # Convert the dataset to a list or dictionary
    dataset = []
    for id, data in enumerate(ds):
        data['id'] = id
        dataset.append(data)

    # If a mapping_key is specified, return a dictionary keyed by that value
    if mapping_key:
        return {item[mapping_key]: item for item in dataset if mapping_key in item}
    else:
        # Otherwise, return the original list of data
        return dataset

def save_to_jsonl(data, output_path):
    # Save data to a JSONL file
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

# Example usage:
data_path = '/gpfs/public/research/tianyu/KOR-Bench/data/NuminaMath-CoT'  # Replace with your dataset path
split = 'train'  # Specify the desired split
output_path = '/gpfs/public/research/tianyu/KOR-Bench/data/NuminaMath-CoT.jsonl'  # Replace with your output file path

# Read data from the Hugging Face dataset
data = read_hf(data_path, split=split)

# Save the data to a JSONL file
save_to_jsonl(data, output_path)
