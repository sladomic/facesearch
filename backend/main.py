from typing import Dict, List
import base64

from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
import requests
import ujson
import os
from sklearn.metrics.pairwise import cosine_similarity

def file2base64(path):
    with open(path, mode='rb') as fl:
        encoded = base64.b64encode(fl.read()).decode('ascii')
        return encoded

app = FastAPI()

with open('trained.json', 'r') as fp:
    trained: Dict = ujson.load(fp)

@app.put("/search/")
def update_item(file: UploadFile):
    candidates: List = []

    try:
        response = requests.post('http://localhost:18081/extract', json={"images": {
            "data": [
                file2base64(file)
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
                                similarity = cosine_similarity(face, trained_image_face)
                                if similarity > 0.6:
                                    candidates.append(trained_image_path)
                                    break

        return candidates

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)