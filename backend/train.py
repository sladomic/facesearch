import os
from typing import Dict
import requests
import ujson
import tqdm

dir_path_local = "/home/ubuntu/InsightFace-REST/src/api_trt/images"
vectors = {}

for filename in tqdm.tqdm(os.listdir(dir_path_local)):
    if "JPG" in filename:
        try:
            response = requests.post('http://localhost:18081/extract', json={"images": {
                "urls": [
                    os.path.join("images", filename)
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