# MLServe - Simple, dockerized serving of Machine Learning models

The goal of this project is to develop a plug&play containerised deployment and serving of the developed Machine Learning models. 

It is done by using (for example, can be any) onnx format for models, Fast API for request, redis for keeping current data and docker for keeping it nice and tight. For now the toy model is CNN MNIST classifier but it can be easily extended for other models and/or regressors/other types.

## How does it work:
Project contains three independent docker containers:
1. `web_api` - front-end container (CLI or streamlit UI) of the project, exposed to outside world for users' requests/input. It's main role is to pass a request to proper, defined model waiting within `model_api` and return results. Take a look into `README.md` in `web_api` for more details.     
2. `model_api` - responsible for model initialization (using onnx runtime session) and communication only with `web_api` for the inputs and results and `db_api` to store current results in redis db and persist them. Take a look into `README.md` in `model_api` for more details.
3. `db_api` - database of the project responsible for keeping current (or all) models results. If one requests again the same input for the same model, the `db_api` will return it's previous value instead of inferencing again the input. It is basically a wrapper of the redis image which is configured for the current setup within network bridge.

Those containers can communicate only within specified docker network bridge `stack_api`  exposing only one port within the `web_api` for the communication with outside world.

## To set up containers:
1. Install docker, docker-compose etc. if necessary
2. Create network bridge for containers: ```docker network create stack_api```
3. Run: ```chmod a+x build_all.sh start_all.sh check_health.sh stop_all.sh``` to turn 'executability' of ```sh``` files
4. Build images by: ```./build_all.sh```
5. Start containers by: ```./start_all.sh APP_TYPE MODEL_NAME```, where `APP_TYPE` and `MODEL_NAME` variables are define below. Basically it starts:
   1. ```model_api``` - container with ```MODEL_NAME``` ready for inference in gpu (or cpu) ```onnx``` session.
   2. ```db_api``` - ```redis``` container which saves inference results according to hexdigest of the ```APP_TYPE``` and selected image name so that if we made an inference twice on the same image we would make one prediction and one would be taken from redis to save for example time.
   3. ```web_api``` - ```fast_api``` if ```APP_TYPE=cli``` or ```streamlit``` if ```APP_TYPE=ui``` container for posting requests for inference and storing/getting them to/from db. Runs on port ```5000``` locally. If:
       1. ```APP_TYPE=ui``` selected you can go to ```localhost:5000``` to use UI
       2. ```APP_TYPE=cli``` post requests via cli (for example: ```python web_api/tests/test_{MODEL_NAME}_cli_request.py {IMAGE_PATH}.png```)
6. You can check whether the containers are running properly by: ```./check_health.sh``` or peek into them by: ```docker logs CONTAINER_NAME```
7. To test containers separately just run: `python tests/{TEST_NAME}.py` within containers dirs.
8. To stop containers just run: ```./stop_all.sh```

## Variables:
   1. ```MODEL_NAME``` for now is available in two options: ```mnist``` and ```leukemia``` if different name is specified container won't start.
   2. ```APP_TYPE``` for now is available in two options: ```ui``` (streamlit) and ```cli``` (usual cmd) if different name is specified container won't start.


## Bonus:
If you get error from ```model_api``` while starting like: ```[...]CUDA failure 999: unknown error[...]``` do the following:
1. ```sudo rmmod nvidia_uvm```
2. ```sudo rmmod nvidia```
3. ```sudo modprobe nvidia```
4. ```sudo modprobe nvidia_uvm```

And try again starting containers.
