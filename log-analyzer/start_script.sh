#!/bin/bash

# Script to copy log analyzer output from Docker container
#!/bin/bash

# 0. Build Docker image
echo "Building Docker image..."
docker build -t log-analyzer .

# 1. Run the container (without --rm)
echo "Starting log-analyzer container..."
docker run -it --name temp-log-analyzer log-analyzer

# 2. Check if container ran successfully
if [ $? -eq 0 ]; then
    echo "Container ran successfully. Copying output file..."
    
    # 3. Create output directory if it doesn't exist
    mkdir -p output
    
    # 4. Copy file from container
    docker cp temp-log-analyzer:/app/output/output.json ./output/
    
    # 5. Check if copy was successful
    if [ $? -eq 0 ]; then
        echo "File copied successfully to ./output/output.json"
        
        # 6. Show file contents
        echo "File contents:"
        cat ./output/output.json | head -n 5
        echo "[...]"
    else
        echo "ERROR: Failed to copy output file"
    fi
    
    # 7. Clean up container
    echo "Removing container..."
    docker rm -f temp-log-analyzer
else
    echo "ERROR: Container failed to run"
fi

# 8. Final check
echo "Verifying output directory:"
ls -lh output/
