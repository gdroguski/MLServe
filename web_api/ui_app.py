import argparse
import io
import hashlib
import redis
import cv2
import numpy as np
import requests
import streamlit as st
from PIL import Image

redis_client = redis.Redis(host='db_api', port=6379)


def _preprocess_image(input_image: io.BytesIO, model_type: str) -> np.ndarray:
    image: Image = Image.open(input_image).convert('RGB')
    image: np.ndarray = np.asarray(image)
    if model_type == 'mnist':
        image: np.ndarray = 1 - cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) / 255.0
        image: np.ndarray = cv2.resize(image, dsize=(28, 28), interpolation=cv2.INTER_CUBIC)
        image: np.ndarray = image.reshape(-1, 28, 28, 1).astype(np.float32)
    elif model_type == 'leukemia':
        image: np.ndarray = cv2.resize(image, dsize=(450, 450), interpolation=cv2.INTER_CUBIC)
        image: np.ndarray = image.reshape(-1, *image.shape[::-1]).astype(np.float32)
    else:
        raise ValueError(f'Unrecognized model_type: {model_type}')

    return image


def classify_image(image_arr: np.ndarray, model_api_url: str) -> dict:
    data: dict = {'image_arr': image_arr.tolist()}

    data_hexdigest = hashlib.sha256(f'ui_{repr(data["image_arr"])}'.encode('utf-8')).hexdigest()
    post_response = redis_client.get(data_hexdigest)
    if post_response:
        post_response = eval(post_response)  # not super safe but for now ok
    else:
        post_response = requests.post(url=model_api_url, json=data)
        post_response = post_response.json()

        redis_client.set(data_hexdigest, str(post_response))

    return post_response


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='specify classification model type: mnist or leukemia', type=str)

    args = parser.parse_args()
    model_type: str = args.model.lower()

    st.set_option('deprecation.showfileUploaderEncoding', False)
    st.title(f'Web API - {model_type}')
    """
    Web API for db_api DB connection and model API onnx runtime session inference
    """

    user_image = st.file_uploader('Insert image here')

    if st.button('Make a prediction'):
        if not user_image:
            st.write('Upload an image first!')
        else:
            _ready_image = _preprocess_image(user_image, model_type)
            prediction = classify_image(_ready_image, 'http://model_api:5050/predict_array')
            st.write('Input image:')
            st.image([user_image], width=300)
            st.write(f'{model_type.capitalize()} prediction json:')
            st.write(prediction)
