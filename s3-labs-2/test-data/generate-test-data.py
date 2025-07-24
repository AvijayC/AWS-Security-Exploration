#!/usr/bin/env python3
import json
import os
import itertools
from datetime import datetime

# Define all possible values
aws_account_ids = ["455095160360", "957401190575"]
access_flags = {
    'access_flag_vpce_a': ['true', 'false'],
    'access_flag_vpce_b': ['true', 'false'],
    'access_flag_no_vpce': ['true', 'false'],
    'access_flag_bucket': ['true', 'false'],
    'access_flag_lambda': ['true', 'false']
}

users = ['awssec-gen-user-1', 'awssec-gen-lambda', 'awssec-b-user-1', 'awssec-b-lambda']

# Generate all permutations
flag_keys = list(access_flags.keys())
flag_values = [access_flags[k] for k in flag_keys]
flag_permutations = list(itertools.product(*flag_values))

# Create manifest data
manifest_data = {"data": []}

# Counter for permutation numbering
perm_counter = 1

# Generate entries for each permutation
for flag_perm in flag_permutations:
    # Create a dictionary for current flag permutation
    current_flags = dict(zip(flag_keys, flag_perm))
    
    # Create readable permission string
    perm_str = []
    if current_flags['access_flag_vpce_a'] == 'true':
        perm_str.append('vpceA')
    if current_flags['access_flag_vpce_b'] == 'true':
        perm_str.append('vpceB')
    if current_flags['access_flag_no_vpce'] == 'true':
        perm_str.append('noVpce')
    if current_flags['access_flag_bucket'] == 'true':
        perm_str.append('bucket')
    
    perm_name = '-'.join(perm_str) if perm_str else 'no-access'
    
    # For each account ID
    for aws_account_id in aws_account_ids:
        # For each user
        for user in users:
            # Create 1 object per combination
            prefix = f"home/{aws_account_id}/{user}/"
            
            # Create descriptive filename
            user_short = user.replace('awssec-', '').replace('-', '_')
            filename = f"perm{perm_counter:02d}_{perm_name}_{user_short}.txt"
            
            # Create manifest entry
            entry = {
                "path": f"./test-objects/{prefix}{filename}",
                "object_key": f"{prefix}{filename}",
                "principal": user,
                "account_id": aws_account_id,
                "tags": {
                    "env": "lab",
                    "lab_name": "s3-labs-2",
                    **current_flags,
                    "permutation_id": f"perm{perm_counter:02d}"
                }
            }
            manifest_data["data"].append(entry)
    
    perm_counter += 1

# Write manifest file
with open('test-data-manifest-complete.json', 'w') as f:
    json.dump(manifest_data, f, indent=4)

# Create test objects directory and files
for entry in manifest_data["data"]:
    filepath = entry["path"]
    tags = entry["tags"]
    principal = entry["principal"]
    account_id = entry["account_id"]
    
    # Ensure the directory for the file exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Create file content with metadata
    content = f"""Test Object Information
======================
Generated: {datetime.now().isoformat()}
Filename: {os.path.basename(filepath)}
Account ID: {account_id}
Principal: {principal}
Permutation ID: {tags['permutation_id']}

Access Flags:
- VPCE A: {tags['access_flag_vpce_a']}
- VPCE B: {tags['access_flag_vpce_b']}
- No VPCE: {tags['access_flag_no_vpce']}
- Bucket: {tags['access_flag_bucket']}
- Lambda: {tags['access_flag_lambda']}

This is test data for S3 access control testing.
"""
    
    # Write the file
    with open(filepath, 'w') as f:
        f.write(content)

print(f"Generated {len(manifest_data['data'])} test objects")
print(f"Total permutations: {len(flag_permutations)}")
print(f"Account IDs: {len(aws_account_ids)}")
print(f"Users: {len(users)}")
print(f"Objects per combination: 1")
print(f"Manifest saved to: test-data-manifest-complete.json")