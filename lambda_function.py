import json
import boto3
import pandas as pd
import io
import traceback

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        print("lambda_handler is running...")

        # Get the S3 bucket name and file key from the Lambda event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print(f"Processing file: {key} from bucket: {bucket}")

        # Fetch the CSV file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        csv_content = response['Body'].read().decode('utf-8')

        # Convert CSV data into a pandas DataFrame
        df = pd.read_csv(io.StringIO(csv_content))
        

        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed {key} from bucket {bucket}, csv length:: {len(df)}')
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing file: {str(e)}")
        }