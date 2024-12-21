from datasets import load_dataset, Features, Value
from datatrove.executor import LocalPipelineExecutor
from datatrove.pipeline.filters import LambdaFilter
from datatrove.pipeline.readers import HuggingFaceDatasetReader
from datatrove.pipeline.readers import JsonlReader
from datatrove.pipeline.writers import JsonlWriter
from datatrove.data import Document, DocumentsPipeline
import dataclasses
import os

import json
from tqdm import tqdm

if __name__ == "__main__":
    def output_adapter(self, document: Document):
        """
        You can create your own adapter that returns a dictionary in your preferred format
        Args:
            document: document to format

        Returns: a dictionary to write to disk

        """
        data = {key: val for key, val in dataclasses.asdict(document).items() if val}
        if self.expand_metadata and "metadata" in data:
            data |= data.pop("metadata")
        output = {
            "token_count": data['metadata']['token_count'],
            "round": data['metadata']['round'],
        }
        return output
        
    # 源数据根目录
    source_root = '/gpfs/public/research/gezhang/fine_grained_cc_data/fine_grained_cc_data_final'
    # 目标根目录
    target_root = '/gpfs/public/research/tianyu/FineFindweb_token'
    
    # 获取所有类别目录
    categories = os.listdir(source_root)
    
    # 遍历每个类别目录
    for category in categories:
        print(f"Processing category: {category}")
        source_path = os.path.join(source_root, category)
        target_path = os.path.join(target_root, category)
        
        # 检查目标目录是否已存在，如果存在则跳过
        if os.path.exists(target_path):
            print(f"Skipping {category} as target directory already exists")
            continue
            
        # 创建目标目录
        os.makedirs(target_path, exist_ok=True)
        
        pipeline_exec = LocalPipelineExecutor(
            pipeline=[
                JsonlReader(data_folder=source_path, file_progress=True, id_key="global_id", text_key="text"),
                JsonlWriter(
                    output_folder=target_path,
                    adapter=output_adapter,
                    compression=None,
                )
            ],
            tasks=32,
        )

        # 运行pipeline
        pipeline_exec.run()
        print(f"Finished processing {category}")
