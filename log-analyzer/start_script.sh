#!/bin/bash

# 0. Ensure the output directory exists on the host machine.
#    The -p flag ensures the command doesn't fail if the directory already exists.
mkdir -p output

# 1. Build the Docker image from the Dockerfile in the current directory.
#    The -t flag tags the image with a name (log-analyzer) for easier reference.
echo "Building Docker image..."
docker build -t log-analyzer .

# 2. Run the container with a mounted volume.
#    --rm -> Automatically removes the container when it exits. This prevents
#            conflicts from old containers if the script is run multiple times.
#    -v "$(pwd)/output:/app/output" -> Maps the host's current directory's 'output' subfolder
#                                      to the '/app/output' directory inside the container.
#                                      Any file the app writes to /app/output will instantly
#                                      appear in ./output on the host.
echo "Starting log-analyzer container..."
docker run --rm -v "$(pwd)/output:/app/output" --name temp-log-analyzer log-analyzer

# 3. Check the exit code of the last command (docker run).
#    An exit code of 0 means the container ran and exited without errors.
if [ $? -eq 0 ]; then
    echo "Container ran successfully."
    echo "Output file should be in the ./output/ directory."

    # 4. Verify the result and display it to the user.
    echo "Verifying output directory:"
    ls -lh output/

    # Check if the expected output file was actually created by the application.
    if [ -f "./output/output.json" ]; then
        echo "File contents:"
        cat ./output/output.json
    else
        echo "WARNING: The application ran, but output.json was not created."
    fi
else
    # A non-zero exit code means the container failed to run.
    echo "ERROR: Container failed to run. Check the logs above for errors from the application."
fi