import os
import boto3
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
import uvicorn

app = FastAPI(
    title="Uplyft Assignment"  # This sets the title of the FastAPI docs
)

# Configure boto3 to use LocalStack
s3 = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    endpoint_url='http://localhost:4566'
)

BUCKET_NAME = "test-bucket-2"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Check file extension
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
        
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit.")
        
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        
        # Upload file to S3 (LocalStack)
        s3.upload_file(file_path, BUCKET_NAME, file.filename)
        
        os.remove(file_path)  # Cleanup temporary file
        
        return {"message": f"File '{file.filename}' uploaded successfully."}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Welcome to the file upload server"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)