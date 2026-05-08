import boto3
import json
from datetime import datetime
from config import AWS_REGION, S3_BUCKET

s3_client = boto3.client('s3', region_name=AWS_REGION)

def upload_file_to_s3(file_name, file_content):
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=f"uploads/{file_name}",
            Body=file_content
        )
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def save_job_status(job_id, status, file_name):
    job_data = {
        "job_id": job_id,
        "status": status,
        "file_name": file_name,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "result": None
    }
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=f"jobs/{job_id}.json",
            Body=json.dumps(job_data, indent=2)
        )
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_job_status(job_id):
    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET,
            Key=f"jobs/{job_id}.json"
        )
        return json.loads(response['Body'].read())
    except Exception as e:
        print(f"Error: {e}")
        return None

def update_job_status(job_id, status, result=None):
    job_data = get_job_status(job_id)
    if not job_data:
        return False
    job_data["status"] = status
    job_data["updated_at"] = datetime.utcnow().isoformat()
    if result:
        job_data["result"] = result
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=f"jobs/{job_id}.json",
            Body=json.dumps(job_data, indent=2)
        )
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def save_result(job_id, result_data):
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=f"results/{job_id}-result.json",
            Body=json.dumps(result_data, indent=2)
        )
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_result(job_id):
    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET,
            Key=f"results/{job_id}-result.json"
        )
        return json.loads(response['Body'].read())
    except Exception as e:
        print(f"Error: {e}")
        return None
