import argparse
import requests
import cv2
import numpy as np


def load_image(image_path: str) -> np.ndarray:
    image_path: str = image_path
    image: np.ndarray = cv2.imread(image_path)
    image: np.ndarray = 1 - cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) / 255.0
    image: np.ndarray = cv2.resize(image, dsize=(28, 28), interpolation=cv2.INTER_CUBIC)
    image: np.ndarray = image.reshape(-1, 28, 28, 1).astype(np.float32)

    return image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", help="specify path for image to classify", type=str)

    args = parser.parse_args()
    image_arr: np.ndarray = load_image(args.img_path)

    data = {'image_arr': image_arr.tolist()}
    post_response = requests.post(url='http://0.0.0.0:5000/web_api', json=data)
    print(post_response)
    print(post_response.json())
