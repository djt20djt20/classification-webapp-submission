from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json
from src import utility_functions 
import logging

app = FastAPI()

class ClassificationRequest(BaseModel):
    query: str
    options: dict
    classes: list

@app.post("/classify")
async def classify_text(request: ClassificationRequest):
    try:
        logging.info("Received request for classification")
        request_data = json.dumps(request.model_dump())
        
        logging.info(f"Request data prepared for processing: {request_data}")
        result = utility_functions.process_request(request_data)
        
        logging.info(f"Received processing result: {result}")
        return result
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
