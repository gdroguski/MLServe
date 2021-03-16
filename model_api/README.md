# Model API container

It's main purpose is to serve and test web API for requests. 

Variable ```MODEL_NAME``` for now is available: ```mnist```, if different name is specified container won't start.

## How to run this separately:

How to run this manually (if you don't want to ```start_all.sh```):
1. ```cd``` here
2. Make some python venv + ```pip install -r requirements.txt``` to have full functionality or just ```pip install numpy requests opencv-python``` to post requests.
3. To test (outside docker):
   1. MNIST model:
      1. ```sudo chmod a+x src/simple_mnist.py``` to enable 'executability' 
      2. ```python src/simple_mnist.py models/mnist.h5 images/mnist.png``` for keras inference
      3. ```python src/simple_mnist.py models/mnist.onnx images/mnist.png``` for onnxruntime inference
   2. Model API app locally:
      1. ```sudo chmod a+x app.py``` to enable 'executability'
      2. ```python app.py {MODEL_NAME}```
      3. ```python tests/test_{MODEL_NAME}_request.py src/{IMAGE}.{EXT}```
4. To build a Docker image: ```docker build -t model_api .``` (`model_api` is just name for image to be built) and wait some time
5. Start docker container with: ```docker run --name model_api --rm --gpus all --net stack_api --mount type=bind,source=/host/path/to/onnx/models,target=/usr/src/model_api/models model_api MODEL_NAME``` (leave ```--rm``` if you want to delete it after closing container)
    1. If daemon needed running in background add ```-d```
    2. If you want to publish port on localhost and expose it to other containers add ``-p`` and ```--net stack_api```
6. To post a request for specified model on localhost's port with given image (assuming it's exposed on localhost):
   1. ```source path_to_venv/bin/activate```
   2. ```python tests/test_{MODEL_NAME}_request.py src/{IMAGE}.{EXT}```
