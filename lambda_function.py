import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        print("lambda_handler is running...")

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print(f"Processing file: {key} from bucket: {bucket}")

        # Fetch the CSV file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        csv_content = response['Body'].read().decode('utf-8')

        # Extract metadata
        file_size = response['ContentLength']  # File size in bytes
        lines = csv_content.strip().split("\n")  # Splitting into lines
        num_lines = len(lines) - 1  # Row count (excluding header)
        column_names = lines[0].split(",")  # Extract column names
        num_columns = len(column_names)  # Column count
        upload_timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp

        metadata = {
            "filename": key,
            "upload_timestamp": upload_timestamp,
            "file_size_bytes": file_size,
            "row_count": num_lines,
            "column_count": num_columns,
            "column_names": column_names
        }

        print(metadata)

        return {
            'statusCode': 200,
            'body': json.dumps(metadata)
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing file: {str(e)}")
        }
