# facesearch

## Setup
This repository is built upon [InsightFace-REST](https://github.com/SthPhoenix/InsightFace-REST).

1. In order to run, clone the repository and place your `images` directory into `InsightFace-REST/models`.
2. Update `InsightFace-REST/deploy_cpu.sh` to use a better detection model `det_model=scrfd_10g_gnkps` instead of `det_model=scrfd_2.5g_gnkps`.
3. Update `InsightFace-REST/deploy_cpu.sh` to use more workers `n_workers=4` instead of `n_workers=1`.
4. Run `InsightFace-REST/deploy_cpu.sh` (you might need to run it twice, since the first time the container is building).
5. Run `cd backend && python build_index.py` to build your index of faces in your existing images.

## Run
1. Run `InsightFace-REST/deploy_cpu.sh` (you might need to run it twice, since the first time the container is building).
2. Run `cd backend && uvicorn main:app --reload`

## Test backend
You can test the backend while running by opening http://localhost:8008/docs#/default/update_item_search__put, then clicking on `Try it out`, choosing a file and clicking on `Execute`.