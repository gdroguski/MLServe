import argparse
import os
from typing import List

import numpy as np
import onnxruntime
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='model_api')

sess = None
input_name = None
output_name = None


class ModelRequest(BaseModel):
    image_arr: List


@app.get('/')
def check_health() -> str:
    return 'Can curl model api!'


def init_onnxruntime(model_path: str) -> None:
    global sess, input_name, output_name
    sess = onnxruntime.InferenceSession(model_path)
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name


@app.post('/predict_array')
def predict_array(request: ModelRequest) -> dict:
    global sess, input_name, output_name
    assert sess

    image: np.ndarray = np.array(request.image_arr).astype(np.float32)
    proba: np.ndarray = sess.run([output_name], {input_name: image})[0]
    cls: int = np.argmax(proba, axis=1)[0]

    print(f'Model\'s classification: {cls} with {round(proba[0, cls], 2)} value')
    result = {
        'cls': int(cls),
        'value': float(proba[0, cls])
    }
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('model_name', help='specify for onnx model: "mnist" or "leukemia"', type=str)

    args = parser.parse_args()

    model_name: str = args.model_name.lower()
    model_file: str = f'/models/{model_name}.onnx'
    if not os.path.isfile(model_file):
        models: list = [model for model in os.listdir("/models") if model.split('.')[-1] == 'onnx']
        raise ValueError(f'Unrecognized onnx model name: {model_name}, available models: {models}')

    init_onnxruntime(model_file)
    uvicorn.run(app, host="0.0.0.0", port=5050)
