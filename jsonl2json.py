import json
def jsonl_to_json(jsonl_file_path):
    json_data = []
    with open(jsonl_file_path, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            json_data.append(json.loads(line))
    
    json_file_path = jsonl_file_path.rsplit('.', 1)[0] + '.json'
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

jsonl_to_json('/gpfs/public/research/gezhang/SHEEP/eamon/plot_data/merged_datasets/merged_difference_1_and_tulu_same_rewrite_tulu.jsonl')