import boto3
import os

s3 = boto3.client('s3')
bucket_name = os.getenv("ai-classroom-material")

def sync_s3_to_rag():
    # Downloads files from S3 to a temporary processing directory
    response = s3.list_objects_v2(Bucket=bucket_name)
    for obj in response.get('Contents', []):
        file_name = obj['Key']
        if file_name.endswith('.pdf'):
            s3.download_file(bucket_name, file_name, f"/tmp/{file_name}")
            # Proceed with indexing from /tmp/

