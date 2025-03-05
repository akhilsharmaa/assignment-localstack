import boto3
import json
import datetime

def lambda_handler(event, context):
    current_time = datetime.datetime.utcnow().isoformat()
    
    if 'Records' in event and event['Records'][0]['eventSource'] == 'aws:s3':
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_name = event['Records'][0]['s3']['object']['key']
        event_source = f"S3 Bucket: {bucket_name}, File: {file_name}"
    else:
        event_source = "Unknown event source"

    response = {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello Bro!!!',
            'time': current_time,
            'event_source': event_source
        })
    }

    print(json.dumps(response))  # 👈 Print the response to capture it in logs
    return response
