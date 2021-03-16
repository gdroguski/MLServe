import argparse

import cv2
import keras
import numpy as np
import onnxruntime


class Mnist:
    def __init__(self, weight_path: str) -> None:
        self.model: keras.Sequential = self._load_model(weight_path)

    def predict(self, instance: np.ndarray) -> np.ndarray:
        return np.argmax(self.model.predict(instance), axis=1)

    def predict_proba(self, instance: np.ndarray) -> np.ndarray:
        return self.model.predict(instance)

    def _load_model(self, h5path: str) -> keras.Sequential:
        model = keras.Sequential()

        model.add(
            keras.layers.Conv2D(filters=32, kernel_size=3, padding='same', activation='relu',
                                input_shape=(28, 28, 1)))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.MaxPooling2D(pool_size=2))
        model.add(keras.layers.Dropout(0.3))

        model.add(keras.layers.Conv2D(filters=64, kernel_size=3, padding='same', activation='relu'))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.MaxPooling2D(pool_size=2))
        model.add(keras.layers.Dropout(0.3))

        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(128, activation='relu'))
        model.add(keras.layers.Dropout(0.5))
        model.add(keras.layers.Dense(10, activation='softmax'))

        model.compile(
            loss=keras.losses.categorical_crossentropy,
            optimizer=keras.optimizers.Adam(),
            metrics=['accuracy']
        )
        model.load_weights(h5path)

        return model


def load_image(image_path: str) -> np.ndarray:
    image_path: str = image_path
    image: np.ndarray = cv2.imread(image_path)
    image: np.ndarray = 1 - cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) / 255.0
    image: np.ndarray = cv2.resize(image, dsize=(28, 28), interpolation=cv2.INTER_CUBIC)
    image: np.ndarray = image.reshape(-1, 28, 28, 1).astype(np.float32)

    return image


def hdf5_predict(model_path: str, image: np.ndarray) -> np.ndarray:
    model: Mnist = Mnist(model_path)
    proba: np.ndarray = model.predict_proba(image)

    return proba


def onnx_predict(model_path: str, image: np.ndarray) -> np.ndarray:
    sess = onnxruntime.InferenceSession(model_path)
    input_name: str = sess.get_inputs()[0].name
    output_name: str = sess.get_outputs()[0].name

    proba: np.ndarray = sess.run([output_name], {input_name: image})[0]

    return proba


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('model_path', help='specify path for onnx model or hdf5 weights', type=str)
    parser.add_argument("img_path", help="specify path for image to classify", type=str)

    args = parser.parse_args()

    image: np.ndarray = load_image(args.img_path)

    model_file: str = args.model_path
    model_type: str = model_file.split('.')[-1].lower()
    if model_type == 'hdf5':
        proba: np.ndarray = hdf5_predict(model_file, image)
    elif model_type == 'onnx':
        proba: np.ndarray = onnx_predict(model_file, image)
    else:
        raise NotImplemented(f'Model_type: {model_type} inference not implemented! Use "onnx" or "hdf5".')

    cls: int = np.argmax(proba, axis=1)[0]
    print(f'Digit classification: {cls} with {round(proba[0, cls] * 100, 2)}% probability')


if __name__ == '__main__':
    main()

