import os
from typing import Dict
import requests
import ujson
import tqdm
from PIL import Image

from utils import resizeAndEncodeImage

dir_path_local = "/home/ubuntu/InsightFace-REST/models/images"
vectors = {}

for filename in tqdm.tqdm(os.listdir(dir_path_local)):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        try:
            image = Image.open(os.path.join(dir_path_local, filename))

            response = requests.post('http://localhost:18081/extract', json={"images": {
                    "data": [
                    resizeAndEncodeImage(image)
                ]
            }})

            if response.status_code == 200:
                content: Dict = ujson.loads(response.content)

                if 'data' in content.keys():
                    data = content["data"][0]
                    
                    path_local = os.path.join(dir_path_local, filename)
                    vectors[path_local] = []
                    for face in data["faces"]:
                        vec = face["vec"]
                        vectors[path_local].append(vec)
                        
        except Exception as e:
            print(e)

with open('trained.json', 'w') as fp:
    ujson.dump(vectors, fp)