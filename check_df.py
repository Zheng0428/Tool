def remove_lines_from_jsonl(file_path, lines_to_remove):
    """
    This function removes specified lines from a JSONL file and saves the modified content back to the same file path.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove the specified lines
    for start_line, end_line in lines_to_remove:
        del lines[start_line-1:end_line]

    # Write the modified content back to the file
    output_file_path = file_path.replace('.jsonl', '_cleaned.jsonl')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# Example usage
file_path = '/gpfs/public/research/gezhang/SHEEP/eamon/plot_data/merged_datasets/merged_difference_1_and_tulu_same_rewrite_tulu.jsonl'
lines_to_remove = [(193195, 193197), (181850, 181854), (187535, 187536)]
remove_lines_from_jsonl(file_path, lines_to_remove)
