import json
import pandas as pd
import pyarrow as pa

def construct_sharegpt_format(input_path, output_path, question_key, response_key):
    """
    Convert a JSONL file to ShareGPT format.
    
    Args:
        input_path (str): Path to input JSONL file
        output_path (str): Path to output JSONL file
        question_key (str): Key name for questions in input data
        response_key (str): Key name for responses in input data
    """
    output_data = []

    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data = json.loads(line)
                
                # Extract question and response
                question = data.get(question_key, '')
                response = data.get(response_key, '')
                
                if not question or not response:
                    print(f"Missing question or response in entry: {data}")
                    continue

                # Construct ShareGPT format
                sharegpt_format = {
                    "conversations": [
                        {
                            "from": "human",
                            "value": question
                        },
                        {
                            "from": "gpt", 
                            "value": response
                        }
                    ]
                }
                
                output_data.append(sharegpt_format)

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                continue

    # Write output file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for entry in output_data:
            outfile.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"Successfully converted {len(output_data)} entries to ShareGPT format")
    print(f"Output saved to {output_path}")

# Example usage
if __name__ == "__main__":
    input_file = "/gpfs/public/research/tianyu/DAG/dataset/NuminaMath/chains_sample_final.jsonl"
    output_file = "/gpfs/public/research/tianyu/DAG/dataset/NuminaMath/chains_sample_final_sharegpt.jsonl" 
    question_key = "problem"
    response_key = "sample_chain_response"
    construct_sharegpt_format(input_file, output_file, question_key, response_key)