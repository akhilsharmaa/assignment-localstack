# SETUP 
#### (Pre-req) Install docker, localstack, aws-cli
```
# Now start localstack in you system 
localstack start  
```

Expected output: 
``` 
     __                     _______ __             __
    / /   ____  _________ _/ / ___// /_____ ______/ /__
   / /   / __ \/ ___/ __ `/ /\__ \/ __/ __ `/ ___/ //_/
  / /___/ /_/ / /__/ /_/ / /___/ / /_/ /_/ / /__/ ,<
 /_____/\____/\___/\__,_/_//____/\__/\__,_/\___/_/|_|

- LocalStack CLI: 4.2.0
- Profile: default
- App: https://app.localstack.cloud

[20:15:16] starting LocalStack in Docker     localstack.py:512
           mode 🐳                                            
─────── LocalStack Runtime Log (press CTRL-C to quit) ────────

LocalStack version: 4.2.1.dev12
LocalStack build date: 2025-03-04
LocalStack build git hash: c596ce031

```
If you are seeing something like this without any error you have install the localstack correctly, & you are good to go. 

---
### Changing Alias 
Instead of pointing the aws-cli to localstack everytime, we will create a alias names `awslocal`, if you are using `zsh` change it accordingly to `.zshrc`
```
echo "alias awslocal='aws --endpoint-url=http://localhost:4566'" >> ~/.bashrc
```
---

### Create a `s3` bucket
This is going to create a bucket named `test-bucket` inside the s3.  
```
awslocal s3 mb s3://test-bucket-2 
```

### (Optional) list all the buckets 
```
awslocal s3 ls        # list all the buckets  
```


### Creating the lambda function 
This is going to create a lambda function named `dummy_lambda_7` with the zip file `lambda-function.zip` and the set runtime as `python3.9`, and other configurations.   
```
awslocal lambda create-function \
  --function-name dummy_lambda_7 \
  --zip-file fileb://lambda-function.zip \
  --handler lambda_function.lambda_handler \
  --runtime python3.9 \
  --role arn:aws:iam::000000000000:role/execution_role
```

### (Optional) Invoking the lamdba function 
check whether the lambda function is working properly, this command return output in `response.json`. check the file content.   

```
awslocal lambda invoke \
    --function-name dummy_lambda_7 \
    --payload '{}' \
    response.json
```


### Add lambda trigger 
Any file uploading in s3 bucket `test-bucket-2` is going to trigger the lambda we have created. above. 
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


---
### IMPORTANT COMMANDS

```
/tmp/lambda/awslambda-us-east-1-tasks/dummy_lambda_4-d68245ec-7b6c-4e1a-8f25-102a05acd56d/code/lambda-function
``` 
# Invoking the lamdba 

```
awslocal lambda invoke \
    --function-name dummy_lambda_7 \
    --payload '{}' \
    response.json
```



### Deleting the lambda function 
```
awslocal lambda delete-function --function-name dummy_lambda_7
```


# Get all cloud watch log groups 
```
awslocal logs describe-log-streams --log-group-name /aws/lambda/dummy_lambda_7 --order-by LastEventTime --descending
```


# Creating the ZIP 
```
zip -r lambda-function.zip lambda_function.py
```


# Dynamically getting the latest log of the lamda 
```
LOG_STREAM=$(awslocal logs describe-log-streams --log-group-name /aws/lambda/dummy_lambda_7 --query 'logStreams[-1].logStreamName' --output text)

awslocal logs get-log-events --log-group-name /aws/lambda/dummy_lambda_7 --log-stream-name "$LOG_STREAM"
```

