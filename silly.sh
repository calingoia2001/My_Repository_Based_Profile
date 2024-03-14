#!/bin/bash

# Define the file path
file_path="/usr/local/test_file.txt"

# Write "test" to the file with elevated privileges
sudo echo "test" > "$file_path"

# Provide feedback
echo "Successfully wrote 'test' to $file_path"
