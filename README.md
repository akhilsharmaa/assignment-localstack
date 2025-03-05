```
/tmp/lambda/awslambda-us-east-1-tasks/dummy_lambda_4-d68245ec-7b6c-4e1a-8f25-102a05acd56d/code/lambda-function
```

# create a s3 bucket
```
awslocal s3 mb s3://test-bucket-2 
```

# Creating the ZIP 
```
zip -r lambda-function.zip lambda_function.py
```

# creating the lambda function 
```
awslocal lambda create-function \
  --function-name dummy_lambda_7 \
  --zip-file fileb://lambda-function.zip \
  --handler lambda_function.lambda_handler \
  --runtime python3.9 \
  --role arn:aws:iam::000000000000:role/execution_role
```

# Invoking the lamdba 

```
awslocal lambda invoke \
    --function-name dummy_lambda_7 \
    --payload '{}' \
    response.json
```


# Add trigger Function 
```
awslocal s3api put-bucket-notification-configuration \
  --bucket test-bucket-2 \
  --notification-configuration '{
    "LambdaFunctionConfigurations": [
      {
        "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:dummy_lambda_7",
        "Events": ["s3:ObjectCreated:*"]
      }
    ]
  }'
```

# Delete Lambda function 
```
awslocal lambda delete-function --function-name dummy_lambda_7
```