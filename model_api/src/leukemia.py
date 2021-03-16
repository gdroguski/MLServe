import argparse

import cv2
import numpy as np
import onnxruntime


def load_image(image_path: str) -> np.ndarray:
    image_path: str = image_path
    image: np.ndarray = cv2.imread(image_path)
    image: np.ndarray = image.reshape(-1, *image.shape[::-1]).astype(np.float32)

    return image


def onnx_predict(model_path: str, image: np.ndarray) -> np.ndarray:
    sess = onnxruntime.InferenceSession(model_path)
    input_name: str = sess.get_inputs()[0].name
    output_name: str = sess.get_outputs()[0].name

    proba: np.ndarray = sess.run([output_name], {input_name: image})[0]

    return proba


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('model_path', help='specify path for onnx model or hdf5 weights', type=str)
    parser.add_argument('img_path', help='specify path for image to classify', type=str)

    args = parser.parse_args()

    image: np.ndarray = load_image(args.img_path)
    model_file: str = args.model_path

    proba: np.ndarray = onnx_predict(model_file, image)
    cls: int = np.argmax(proba, axis=1)[0]

    print(f'Leukemia classification: {cls} with {round(proba[0, cls], 2)} logit value')


if __name__ == '__main__':
    main()
