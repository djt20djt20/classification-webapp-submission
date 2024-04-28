from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json
from src import utility_functions 

app = FastAPI()

class ClassificationRequest(BaseModel):
    query: str
    options: dict
    classes: list

@app.post("/classify/")
async def classify_text(request: ClassificationRequest):
    try:
        request_data = json.dumps(request.dump())
        result = utility_functions.process_request(request_data)
        return result
    except Exception as e:
        print('here error')
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
