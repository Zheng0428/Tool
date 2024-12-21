#!/bin/bash

# Usage: ./retry_huggingface_download.sh [huggingface-cli download args]
# Example: ./retry_huggingface_download.sh model_name --revision main

# Function to perform the download with retries
retry_download() {
  local retries=5   # Number of retries
  local wait_time=10 # Wait time between retries (in seconds)
  local count=0

  while [ $count -lt $retries ]; do
    echo "Attempt $(($count + 1))..."

    # Run the huggingface-cli download command with passed arguments
    huggingface-cli download "$@"

    # Check if the command was successful
    if [ $? -eq 0 ]; then
      echo "Download successful!"
      return 0
    fi

    echo "Download failed. Retrying in $wait_time seconds..."
    sleep $wait_time
    count=$(($count + 1))
  done

  echo "Download failed after $retries attempts."
  return 1
}

# Call the function with all passed arguments
retry_download "$@"
