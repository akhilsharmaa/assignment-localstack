import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = "files-db" 

def create_table_if_not_exist(): 
    try:
        response = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "filename", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "filename", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST"
        )
        print("Table creation started:", response)
    except Exception as e:
        print("Error creating table:", str(e))

def write_to_dynamodb(data):
    try:
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item=data)

        print("Data successfully written to DynamoDB")
    except Exception as e:
        print(f"Error writing to DynamoDB: {str(e)}")
            

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
        file_size = response['ContentLength']  
        lines = csv_content.strip().split("\n") 
        num_lines = len(lines) - 1  
        column_names = lines[0].split(",") 
        num_columns = len(column_names) 
        upload_timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        metadata = {
            "filename": key,
            "upload_timestamp": upload_timestamp,
            "file_size_bytes": file_size,
            "row_count": num_lines,
            "column_count": num_columns,
            "column_names": column_names
        }

        create_table_if_not_exist(); 
        write_to_dynamodb(metadata)

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
