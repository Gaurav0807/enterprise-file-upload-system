from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uuid
from config import API_HOST, API_PORT
from s3_utils import (
    upload_file_to_s3, save_job_status, get_job_status,
    update_job_status, save_result, get_result
)
from processor import process_csv

app = FastAPI(title="File Processor API", version="1.0.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        job_id = str(uuid.uuid4())
        
        upload_file_to_s3(f"{job_id}.csv", content)
        save_job_status(job_id, "processing", file.filename)
        
        result = process_csv(content)
        
        if "error" not in result:
            save_result(job_id, result)
            update_job_status(job_id, "completed", result)
        else:
            update_job_status(job_id, "failed", result)
        
        return {
            "job_id": job_id,
            "file_name": file.filename,
            "status": "completed",
            "result": result
        }
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/status/{job_id}")
def get_status(job_id: str):
    try:
        job = get_job_status(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/results/{job_id}")
def get_results(job_id: str):
    try:
        result = get_result(job_id)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
