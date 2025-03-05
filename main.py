import boto3
import os

# Configure boto3 to use LocalStack
s3 = boto3.client('s3',
                region_name='us-east-1',
                aws_access_key_id='test',
                aws_secret_access_key='test',
                endpoint_url='http://localhost:4566'
            )

bucket_name = 'test-bucket-2'
image_path = './data/test24mb.csv'
image_key = os.path.basename(image_path)

try:
    s3.upload_file(image_path, bucket_name, image_key)
    print(f"Image {image_path} uploaded to bucket {bucket_name} as {image_key}.")
except Exception as e:
    print(f"Error uploading image: {e}")
