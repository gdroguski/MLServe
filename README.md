# How to run this:

## Variables:
   1. ```MODEL_NAME``` for now is available in two options: ```mnist``` and ```leukemia``` if different name is specified container won't start.
   2. ```APP_TYPE``` for now is available in two options: ```ui``` (streamlit) and ```cli``` (usual cmd) if different name is specified container won't start.

## To set up containers:
1. Install docker, docker-compose etc.
2. Create network bridge for containers: ```docker network create stack_api```
3. Run: ```chmod a+x build_all.sh start_all.sh check_health.sh stop_all.sh``` to turn 'executability of ```sh``` files
2. Build images by: ```./build_all.sh```
3. Start containers by: ```./start_all.sh APP_TYPE MODEL_NAME```. Basically it starts:
   1. ```model_api``` - container with ```MODEL_NAME``` ready for inference in gpu ```onnx``` session.
   2. ```db_api``` - ```redis``` container which saves inference results according to hexdigest of the ```APP_TYPE``` and selected image name so that if we made an inference twice on the same image we would make one prediction and one would be taken from redis to save for example time.
   3. ```web_api``` - ```fast_api``` if ```APP_TYPE=cli``` or ```streamlit``` if ```APP_TYPE=ui``` container for posting requests for inference and storing/getting them to/from db. Runs on port ```5000``` locally. If:
       1. ```APP_TYPE=ui``` selected you can go to ```localhost:5000``` to use UI
       2. ```APP_TYPE=cli``` post requests via cli (for example: ```python web_api/tests/test_{MODEL_NAME}_cli_request.py {IMAGE_PATH}.png```)
4. You can check whether the containers are running properly by: ```./check_health.sh``` or peek into them by: ```docker logs CONTAINER_NAME```
5. To stop containers just run: ```./stop_all.sh```

## Bonus:
If you get error from ```model_api``` while starting like: ```[...]CUDA failure 999: unknown error[...]``` do the following:
1. ```sudo rmmod nvidia_uvm```
2. ```sudo rmmod nvidia```
3. ```sudo modprobe nvidia```
4. ```sudo modprobe nvidia_uvm```

And try again starting containers.
