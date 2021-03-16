import hashlib
from typing import List

import redis
import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='web_api')
redis_client = redis.Redis(host='db_api', port=6379)


class ModelRequest(BaseModel):
    image_arr: List


@app.get('/')
def check_access() -> str:
    return 'Can curl web api!'


@app.post('/web_api')
def post_route(request: ModelRequest) -> dict:
    data_hexdigest = hashlib.sha256(f'cli_{repr(request.image_arr)}'.encode('utf-8')).hexdigest()
    post_response = redis_client.get(data_hexdigest)
    if post_response:
        post_response = eval(post_response)  # not super safe but for now ok
    else:
        data = {'image_arr': request.image_arr}
        post_response = requests.post(url='http://model_api:5050/predict_array', json=data)
        post_response = post_response.json()

        redis_client.set(data_hexdigest, str(post_response))

    return post_response


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
