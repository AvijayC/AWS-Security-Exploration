#!/usr/bin/env python3
"""
Upload test data to all 6 S3 buckets
"""

import subprocess
import sys
import time

# Define all buckets
buckets = [
    "avijay-lab-1-sse-s3",
    "avijay-lab-2-sse-kms",
    "avijay-lab-3-sse-s3-vpce-a",
    "avijay-lab-4-sse-kms-vpce-a",
    "avijay-lab-5-sse-s3-vpce-b",
    "avijay-lab-6-sse-kms-vpce-b"
]

def upload_to_bucket(bucket_name):
    """Upload test data to a single bucket"""
    print(f"\n{'='*60}")
    print(f"Uploading to bucket: {bucket_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Run the upload script
        result = subprocess.run(
            [sys.executable, "upload-test-data.py", bucket_name],
            capture_output=True,
            text=True
        )
        
        # Print output
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"\n✅ Successfully uploaded to {bucket_name} in {elapsed:.2f} seconds")
            return True
        else:
            print(f"\n❌ Failed to upload to {bucket_name}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error uploading to {bucket_name}: {str(e)}")
        return False

def main():
    print("Starting batch upload to all 6 buckets")
    print(f"Total buckets: {len(buckets)}")
    print(f"Total files per bucket: 192")
    print(f"Total files to upload: {len(buckets) * 192}")
    
    overall_start = time.time()
    successful_buckets = []
    failed_buckets = []
    
    for i, bucket in enumerate(buckets, 1):
        print(f"\n[{i}/{len(buckets)}] Processing {bucket}...")
        
        if upload_to_bucket(bucket):
            successful_buckets.append(bucket)
        else:
            failed_buckets.append(bucket)
    
    # Final summary
    overall_elapsed = time.time() - overall_start
    
    print("\n" + "="*60)
    print("BATCH UPLOAD COMPLETE")
    print("="*60)
    print(f"Total time: {overall_elapsed:.2f} seconds ({overall_elapsed/60:.1f} minutes)")
    print(f"Successful buckets: {len(successful_buckets)}/{len(buckets)}")
    
    if successful_buckets:
        print("\n✅ Successfully uploaded to:")
        for bucket in successful_buckets:
            print(f"   - {bucket}")
    
    if failed_buckets:
        print("\n❌ Failed uploads:")
        for bucket in failed_buckets:
            print(f"   - {bucket}")
        sys.exit(1)
    else:
        print("\n🎉 All uploads completed successfully!")

if __name__ == "__main__":
    main()