#!/bin/bash

# Upload script for test data with tags from manifest
# Usage: ./upload-test-data.sh <bucket-name>

if [ -z "$1" ]; then
    echo "Usage: $0 <bucket-name>"
    echo "Example: $0 avijay-lab-1-sse-s3"
    exit 1
fi

BUCKET_NAME=$1
PROFILE="awssec-gen-admin"
MANIFEST_FILE="test-data-manifest-complete.json"

echo "Uploading test objects to bucket: $BUCKET_NAME"
echo "Using profile: $PROFILE"
echo "Reading manifest: $MANIFEST_FILE"
echo ""

# Check if manifest exists
if [ ! -f "$MANIFEST_FILE" ]; then
    echo "Error: Manifest file not found: $MANIFEST_FILE"
    echo "Please run generate-test-data.py first"
    exit 1
fi

# Parse the manifest and upload each file
# Using Python to parse JSON and generate upload commands
python3 << 'EOF'
import json
import subprocess
import sys
import os

bucket_name = sys.argv[1]
profile = sys.argv[2]
manifest_file = sys.argv[3]

# Read manifest
with open(manifest_file, 'r') as f:
    manifest = json.load(f)

total_files = len(manifest['data'])
uploaded = 0
failed = 0

print(f"Total files to upload: {total_files}")
print("-" * 50)

for entry in manifest['data']:
    file_path = entry['path']
    object_key = entry['object_key']
    tags = entry['tags']
    
    # Build tagging string
    tag_list = []
    for key, value in tags.items():
        # AWS CLI expects URL-encoded format for tags
        tag_list.append(f"{key}={value}")
    
    tagging_string = "&".join(tag_list)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        failed += 1
        continue
    
    # Build AWS CLI command
    cmd = [
        'aws', 's3', 'cp',
        file_path,
        f's3://{bucket_name}/{object_key}',
        '--tagging', tagging_string,
        '--profile', profile
    ]
    
    # Execute upload
    print(f"Uploading: {os.path.basename(file_path)} ... ", end='', flush=True)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("SUCCESS")
            uploaded += 1
        else:
            print(f"FAILED: {result.stderr}")
            failed += 1
    except Exception as e:
        print(f"ERROR: {str(e)}")
        failed += 1

print("-" * 50)
print(f"Upload complete!")
print(f"Successfully uploaded: {uploaded}/{total_files}")
if failed > 0:
    print(f"Failed uploads: {failed}")
    sys.exit(1)
EOF $BUCKET_NAME $PROFILE $MANIFEST_FILE