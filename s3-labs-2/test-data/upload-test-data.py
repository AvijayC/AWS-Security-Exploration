#!/usr/bin/env python3
"""
Upload test data files to S3 with tags from manifest file.
Provides better error handling and progress tracking than shell script.
"""

import json
import sys
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class S3Uploader:
    def __init__(self, bucket_name, profile_name='awssec-gen-admin'):
        self.bucket_name = bucket_name
        self.profile_name = profile_name
        self.session = boto3.Session(profile_name=profile_name)
        self.s3_client = self.session.client('s3')
        self.failed_uploads = []
        self.successful_uploads = []
        
    def upload_file(self, file_path, object_key, tags):
        """Upload a single file with tags."""
        try:
            # Convert tags dict to URL-encoded string format required by S3
            tag_pairs = [f"{k}={v}" for k, v in tags.items()]
            tagging_string = "&".join(tag_pairs)
            
            # Upload file
            with open(file_path, 'rb') as f:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_key,
                    Body=f,
                    Tagging=tagging_string
                )
            
            return True, f"Successfully uploaded: {object_key}"
            
        except FileNotFoundError:
            return False, f"File not found: {file_path}"
        except ClientError as e:
            error_code = e.response['Error']['Code']
            return False, f"AWS Error uploading {object_key}: {error_code} - {e.response['Error']['Message']}"
        except Exception as e:
            return False, f"Unexpected error uploading {object_key}: {str(e)}"
    
    def upload_batch(self, entries, max_workers=10):
        """Upload multiple files concurrently."""
        total = len(entries)
        completed = 0
        
        print(f"\nStarting upload of {total} files to bucket: {self.bucket_name}")
        print(f"Using profile: {self.profile_name}")
        print(f"Max concurrent uploads: {max_workers}")
        print("-" * 60)
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all upload tasks
            future_to_entry = {
                executor.submit(
                    self.upload_file, 
                    entry['path'], 
                    entry['object_key'], 
                    entry['tags']
                ): entry for entry in entries
            }
            
            # Process completed uploads
            for future in as_completed(future_to_entry):
                entry = future_to_entry[future]
                completed += 1
                
                try:
                    success, message = future.result()
                    
                    if success:
                        self.successful_uploads.append(entry['object_key'])
                        status = "✓"
                    else:
                        self.failed_uploads.append({
                            'object_key': entry['object_key'],
                            'error': message
                        })
                        status = "✗"
                    
                    # Progress indicator
                    progress = f"[{completed}/{total}]"
                    print(f"{progress:>10} {status} {os.path.basename(entry['object_key']):<40} {message}")
                    
                except Exception as e:
                    self.failed_uploads.append({
                        'object_key': entry['object_key'],
                        'error': str(e)
                    })
                    print(f"[{completed}/{total}] ✗ {entry['object_key']} - Unexpected error: {str(e)}")
        
        elapsed_time = time.time() - start_time
        return elapsed_time

def main():
    parser = argparse.ArgumentParser(description='Upload test data to S3 with tags')
    parser.add_argument('bucket_name', help='Target S3 bucket name')
    parser.add_argument('--profile', default='awssec-gen-admin', help='AWS profile to use')
    parser.add_argument('--manifest', default='test-data-manifest-complete.json', help='Manifest file path')
    parser.add_argument('--max-workers', type=int, default=10, help='Maximum concurrent uploads')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be uploaded without uploading')
    
    args = parser.parse_args()
    
    # Load manifest
    if not os.path.exists(args.manifest):
        print(f"Error: Manifest file not found: {args.manifest}")
        print("Please run generate-test-data.py first")
        sys.exit(1)
    
    with open(args.manifest, 'r') as f:
        manifest = json.load(f)
    
    entries = manifest['data']
    
    if args.dry_run:
        print(f"DRY RUN: Would upload {len(entries)} files to bucket: {args.bucket_name}")
        print("\nSample files that would be uploaded:")
        for i, entry in enumerate(entries[:5]):
            print(f"  - {entry['object_key']}")
        if len(entries) > 5:
            print(f"  ... and {len(entries) - 5} more files")
        return
    
    # Create uploader and perform upload
    uploader = S3Uploader(args.bucket_name, args.profile)
    
    try:
        # Test credentials
        uploader.s3_client.head_bucket(Bucket=args.bucket_name)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"Error: Bucket '{args.bucket_name}' not found")
        elif error_code == '403':
            print(f"Error: Access denied to bucket '{args.bucket_name}'")
        else:
            print(f"Error accessing bucket: {error_code}")
        sys.exit(1)
    except NoCredentialsError:
        print(f"Error: No credentials found for profile '{args.profile}'")
        sys.exit(1)
    
    # Perform upload
    elapsed_time = uploader.upload_batch(entries, max_workers=args.max_workers)
    
    # Summary
    print("\n" + "=" * 60)
    print("UPLOAD SUMMARY")
    print("=" * 60)
    print(f"Total files: {len(entries)}")
    print(f"Successful: {len(uploader.successful_uploads)}")
    print(f"Failed: {len(uploader.failed_uploads)}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Average speed: {len(entries) / elapsed_time:.2f} files/second")
    
    if uploader.failed_uploads:
        print("\nFAILED UPLOADS:")
        for failure in uploader.failed_uploads[:10]:  # Show first 10 failures
            print(f"  - {failure['object_key']}: {failure['error']}")
        if len(uploader.failed_uploads) > 10:
            print(f"  ... and {len(uploader.failed_uploads) - 10} more failures")
        
        # Save failed uploads to file
        with open('failed-uploads.json', 'w') as f:
            json.dump(uploader.failed_uploads, f, indent=2)
        print(f"\nFailed uploads saved to: failed-uploads.json")
        sys.exit(1)
    else:
        print("\n✅ All files uploaded successfully!")

if __name__ == '__main__':
    main()