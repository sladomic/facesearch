import base64
from typing import Dict

import os
from PIL import Image
import uvicorn
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import ujson
import io
from sklearn.metrics.pairwise import cosine_similarity

from utils import resizeAndEncodeImage

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://ec2-18-222-149-34.us-east-2.compute.amazonaws.com:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('/home/ubuntu/facesearch/backend/trained.json', 'r') as fp:
    trained: Dict = ujson.load(fp)

@app.put("/search/")
def update_item(uploadFile: UploadFile):
    candidates: Dict = {}

    image = Image.open(io.BytesIO(uploadFile.file.read()))

    try:
        response = requests.post('http://localhost:18081/extract', json={"images": {
            "data": [
                resizeAndEncodeImage(image)
            ]
        }})

        if response.status_code == 200:
                content: Dict = ujson.loads(response.content)

                if 'data' in content.keys():
                    data = content["data"][0]
                    
                    for face in data["faces"]:
                        vec = face["vec"]

                        for trained_image_path, trained_image_faces in trained.items():
                            for trained_image_face in trained_image_faces:
                                similarity = cosine_similarity([vec], [trained_image_face])
                                if similarity > 0.6:
                                    trained_image = Image.open(trained_image_path)
                                    trained_image_file = io.BytesIO()
                                    trained_image.save(trained_image_file, format="JPEG")
                                    encoded = base64.b64encode(trained_image_file.getvalue()).decode('ascii')
                                    candidates[os.path.basename(trained_image_path)] = encoded
                                    break

        return candidates

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)