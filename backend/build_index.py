from multiprocessing import Pool as ProcessPool
import os
from typing import Dict
import requests
import ujson
import tqdm
from PIL import Image

from utils import resizeAndEncodeImage

dir_path_local = "/home/ubuntu/InsightFace-REST/models/images"
filepaths = []
vectors = {}

def process_file(filepath):
    try:
        image = Image.open(filepath)

        response = requests.post('http://localhost:18081/extract', json={"images": {
                "data": [
                resizeAndEncodeImage(image)
            ]
        }})

        if response.status_code == 200:
            content: Dict = ujson.loads(response.content)

            if 'data' in content.keys():
                data = content["data"][0]
                
                _vectors = []
                for face in data["faces"]:
                    vec = face["vec"]
                    _vectors.append(vec)

                return {
                    filepath: _vectors
                }
                    
    except Exception as e:
        print(e)

for filename in os.listdir(dir_path_local):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        filepaths.append(os.path.join(dir_path_local, filename))

with ProcessPool(20) as p:
    for _vectors in tqdm.tqdm(p.imap_unordered(process_file, filepaths), total=len(filepaths)):
        vectors = vectors | _vectors

with open('trained.json', 'w') as fp:
    ujson.dump(vectors, fp)