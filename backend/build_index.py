from multiprocessing import Pool as ProcessPool
import os
from typing import Dict
import requests
import ujson
import tqdm
from PIL import Image
import time

from utils import resizeAndEncodeImage

dir_path_local = "/home/ubuntu/InsightFace-REST/models/images"
filepaths = []
vectors = {}

def process_file(filepath):
    _vectors = []

    # Try 3 times (with 1 second in between), sometimes there's a connection problem with the InsightFace-REST API
    for attempt in range(3):
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
                    
                    for face in data["faces"]:
                        vec = face["vec"]
                        _vectors.append(vec)

                    
                        
        except Exception:
            time.sleep(1)
            continue

        break

    return { filepath: _vectors }
    

for filename in os.listdir(dir_path_local):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        filepaths.append(os.path.join(dir_path_local, filename))

with ProcessPool(4) as p:
    for _vectors in tqdm.tqdm(p.imap_unordered(process_file, filepaths), total=len(filepaths)):
        vectors = vectors | _vectors

with open('trained.json', 'w') as fp:
    ujson.dump(vectors, fp)