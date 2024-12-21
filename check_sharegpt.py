import json
import pandas as pd
import pyarrow as pa

def check_sharegpt_format(file_path, output_path):
    """
    This function checks if a given JSONL file follows the ShareGPT format.
    The ShareGPT format requires that each entry in the JSONL file has a "conversations" key,
    and each conversation must have a "from" key with values "system", "human", or "gpt".
    Additionally, it checks if the "from" values alternate between "human" and "gpt",
    and "system" can only appear in the first position or not at all.
    It also checks if the "conversations" key contains a list.
    Furthermore, it checks if all values in the conversations are strings.
    """
    valid_from_values = {"system", "human", "gpt"}
    valid_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data = json.loads(line)
                if "conversations" not in data:
                    print(f"Missing 'conversations' key in entry: {data}")
                    continue

                conversations = data["conversations"]
                if not isinstance(conversations, list):
                    print(f"'conversations' is not a list in entry: {data}")
                    continue

                if conversations and conversations[0].get("from") == "system":
                    conversations = conversations[1:]

                previous_from = None
                human_gpt_pair = True
                for conversation in conversations:
                    if "from" not in conversation:
                        print(f"Missing 'from' key in conversation: {conversation}")
                        human_gpt_pair = False
                        break
                    if conversation["from"] not in valid_from_values:
                        print(f"Invalid 'from' value in conversation: {conversation}")
                        human_gpt_pair = False
                        break
                    if previous_from == conversation["from"]:
                        print(f"'from' values do not alternate in conversation: {conversation}")
                        human_gpt_pair = False
                        break
                    if previous_from == "human" and conversation["from"] != "gpt":
                        human_gpt_pair = False
                    if previous_from == "gpt" and conversation["from"] != "human":
                        human_gpt_pair = False
                    previous_from = conversation["from"]

                    # Check if all values in the conversation are strings
                    for key, value in conversation.items():
                        if not isinstance(value, str):
                            print(f"Value for key '{key}' is not a string in conversation: {conversation}")
                            human_gpt_pair = False
                            break

                if not human_gpt_pair:
                    print(f"Human/GPT pairs do not appear correctly in entry: {data}")
                    continue

                valid_data.append(data)

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                continue

    with open(output_path, 'w', encoding='utf-8') as output_file:
        for entry in valid_data:
            output_file.write(json.dumps(entry) + '\n')

    print("The file follows the ShareGPT format.")
    return True

def convert_to_arrow(file_path):
    """
    This function attempts to convert a JSONL file to an Arrow Table to check for conversion errors.
    """
    try:
        df = pd.read_json(file_path, lines=True)
        # Check each column for mixed types
        for column in df.columns:
            if df[column].apply(lambda x: isinstance(x, list)).any() and df[column].apply(lambda x: not isinstance(x, list) and pd.notna(x)).any():
                print(f"Column '{column}' has mixed list and non-list values.")
                problematic_rows = df[df[column].apply(lambda x: isinstance(x, list)) & df[column].apply(lambda x: not isinstance(x, list) and pd.notna(x))]
                print(f"Problematic rows in column '{column}':\n{problematic_rows}")
        
        table = pa.Table.from_pandas(df)
        print("Successfully converted to Arrow Table.")
    except Exception as e:
        print(f"Failed to convert to Arrow Table: {e}")
        # Print the problematic data
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data = json.loads(line)  # Attempt to load each line to find the problematic one
                    if isinstance(data.get("conversations"), list):
                        for conversation in data["conversations"]:
                            if not isinstance(conversation, dict):
                                print(f"Invalid conversation format: {conversation}")
                except json.JSONDecodeError:
                    print(f"Invalid JSON line: {line.strip()}")
                except Exception as inner_e:
                    print(f"Error processing line: {line.strip()} - {inner_e}")

# Example usage
file_path = '/gpfs/public/research/gezhang/SHEEP/eamon/plot_data/merged_datasets/merged_bge_remove_07_and_tulu_same_rewrite_mixture.jsonl'
output_path = '/gpfs/public/research/gezhang/SHEEP/eamon/plot_data/merged_datasets/merged_bge_remove_07_and_tulu_same_rewrite_mixture.jsonl'
check_sharegpt_format(file_path, output_path)
convert_to_arrow(output_path)