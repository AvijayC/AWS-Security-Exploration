# S3 Labs Test Data - Context for Claude

## Project Overview
This directory contains test data generation and upload scripts for AWS S3 security labs. The goal is to create comprehensive test objects with various access control flags to test S3 permissions, VPC endpoints, and identity-based access controls.

## Key Files

### Generated Test Data
- `test-data-manifest-complete.json` - Complete manifest with 192 test objects and their tags
- `test-objects/` - Directory containing 192 test files with descriptive names
- `test-data-manifest.json` - Original sample manifest (1 object example)

### Scripts
- `generate-test-data.py` - Generates all test objects and manifest
- `upload-test-data.py` - Uploads objects to single S3 bucket with proper tagging
- `upload-to-all-buckets.py` - Batch uploads to all 6 S3 buckets
- `upload-test-data.sh` - Shell script version (deprecated, use Python version)

### Configuration
- `requirements.txt` - Python dependencies (boto3, botocore)

## Test Data Structure

### Access Flags (16 permutations total)
- `access_flag_vpce_a`: true/false - Access via VPC Endpoint A
- `access_flag_vpce_b`: true/false - Access via VPC Endpoint B  
- `access_flag_no_vpce`: true/false - Access without VPC Endpoint
- `access_flag_bucket`: true/false - Bucket-level access allowed

### Users (4 types)
- `awssec-gen-user-1` - General user 1
- `awssec-gen-lambda` - General Lambda function
- `awssec-b-user-1` - Business user 1
- `awssec-b-lambda` - Business Lambda function

### Object Generation
- **16 flag permutations** × **4 users** × **3 objects each** = **192 total objects**
- Each object tagged with: env, lab_name, access flags, user, permutation_id, object_number

## S3 Buckets Used
All 6 buckets contain the same 192 test objects:
1. `avijay-lab-1-sse-s3`
2. `avijay-lab-2-sse-kms`
3. `avijay-lab-3-sse-s3-vpce-a`
4. `avijay-lab-4-sse-kms-vpce-a`
5. `avijay-lab-5-sse-s3-vpce-b`
6. `avijay-lab-6-sse-kms-vpce-b`

## File Naming Convention
Format: `perm{ID}_{access-flags}_{user}_{object-num}.txt`

Examples:
- `perm01_vpceA-vpceB-noVpce-bucket_gen_user_1_1.txt`
- `perm16_no-access_b_lambda_3.txt`

## AWS Profile
- Profile used: `awssec-gen-admin`
- Region: `us-east-1`

## Usage Commands

### Generate test data
```bash
python3 generate-test-data.py
```

### Upload to single bucket
```bash
python3 upload-test-data.py <bucket-name>
python3 upload-test-data.py avijay-lab-1-sse-s3 --dry-run
```

### Upload to all buckets
```bash
python3 upload-to-all-buckets.py
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## Test Object Content
Each test file contains:
- Generation timestamp
- Filename and metadata
- Associated user
- Access flag values
- Permutation information

## Testing Strategy
This test data enables testing:
- VPC Endpoint access controls (vpce_a, vpce_b flags)
- Internet vs VPC Endpoint access (no_vpce flag)
- Bucket-level vs object-level permissions (bucket flag)
- Identity-based access (different users)
- SSE-S3 vs SSE-KMS encryption (different bucket types)

## Last Updated
Generated and uploaded: July 23, 2025
Total objects per bucket: 192
Total objects across all buckets: 1,152