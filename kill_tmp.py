import os
import shutil

def delete_old_checkpoints(base_path: str):
    for model_dir in os.listdir(base_path):
        model_path = os.path.join(base_path, model_dir)
        if os.path.isdir(model_path):
            checkpoint_dirs = [d for d in os.listdir(model_path) if d.startswith("checkpoint-") and os.path.isdir(os.path.join(model_path, d))]
            if checkpoint_dirs:
                # Extract step numbers and find the maximum step
                steps = [int(d.split('-')[1]) for d in checkpoint_dirs]
                max_step = max(steps)
                # Delete all checkpoint directories except the one with the maximum step
                for checkpoint_dir in checkpoint_dirs:
                    step = int(checkpoint_dir.split('-')[1])
                    if step != max_step:
                        checkpoint_path = os.path.join(model_path, checkpoint_dir)
                        shutil.rmtree(checkpoint_path)
                        print(f"Deleted: {checkpoint_path}")

# Example usage
delete_old_checkpoints("/gpfs/public/research/junpeng/checkpoints")
