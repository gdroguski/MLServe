Simple web_api which communicates with closed ```model_api``` and ```redis``` containers. 
Basically here you post requests for predictions to get them from the model or from the DB if there is already a prediction in there - based on hexdigest of the image.

Variable:
   1. ```MODEL_NAME``` for now is available in two options: ```mnist``` and ```leukemia``` if different name is specified container won't start.
   2. ```APP_TYPE``` for now is available in two options: ```ui``` (streamlit) and ```cli``` (usual cmd) if different name is specified container won't start.

How to run this manually (if you don't want to ```start_all.sh```):
1. ```cd``` here
2. ```docker build -t web_api .```
3. ```docker run --rm --name web_api -p 5000:5000 --net stack_api -t -i web_api APP_TYPE MODEL_TYPE``` (leave ```--rm``` if you want to delete it after closing container)
4. Check posts requesting by running twice ```python test_request.py ../model_api/src/img.png``` - first one should make prediction in ```model_api``` conainer and the second one should get it's already existing prediction from the db handled by ```redis``` container.
