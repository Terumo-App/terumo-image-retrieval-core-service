from fastapi import FastAPI, File, UploadFile,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import base64
import io
from PIL import Image
from api.schema.schemas import HealthCheckResult
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Creating an app object
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImagePayload(BaseModel):
    image: dict

# Default route
@app.post("/image-query")
async def process_image(body: ImagePayload):
    if  'data' not in body.image.keys():
        raise HTTPException(status_code=400, detail="No image data provided")
    

    # Make a POST request to another endpoint with the image data and format
    model_urls = [
        # "http://service-model-a:5000/predict",
        "http://localhost:5000/predict",

        ]
    
    payload = {
        "image": {
            "data": body.image['data'],
            "format": body.image['format']
        }
    }
    headers = {
        "Content-Type": "application/json"
    }

    # Calling model apis 
    responses = []
    for url in model_urls:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=res.text)
        responses.extend(res.json())

    # formating for search engine request



    print(responses)
    # url = "http://service-search:5003/attribute-query"
    # res = requests.post(url, headers=headers, json={"data": 1 })
    # data = res.json()
    # print(data)


    return {'message': 'Image processed successfully', 'result':responses}


@app.get("/health", response_model=HealthCheckResult)
async def health_check() -> HealthCheckResult:
    return HealthCheckResult(success=True)