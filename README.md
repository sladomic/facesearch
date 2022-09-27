# facesearch

## Setup
This repository is built upon [InsightFace-REST](https://github.com/SthPhoenix/InsightFace-REST).

1. In order to run, clone the repository and place your `images` directory into `InsightFace-REST/models`.
2. Run `cd backend && python train.py` to build your index of faces in your existing images.

## Run
1. Run `InsightFace-REST/deploy_cpu.sh` (you might need to run it twice, since the first time the container is building).
2. Run `cd backend && uvicorn main:app --reload`

## Test backend
You can test the backend while running by opening http://localhost:8008/docs#/default/update_item_search__put, then clicking on `Try it out`, choosing a file and clicking on `Execute`.