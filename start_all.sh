#!/bin/bash
APP_TYPE=$1
MODEL_TYPE=$2

BASE_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker run --name model_api --rm -d \
       --gpus all --net stack_api \
       --mount type=bind,source="$BASE_PATH"/model_api/models,target=/models \
       model_api "$MODEL_TYPE"
echo "Model_API with '$MODEL_TYPE' started"

docker run --name db_api --rm -d \
       --net stack_api \
       --mount type=bind,source="$BASE_PATH"/db_api/data,target=/data \
       db_api
echo "DB_API started"

docker run --name web_api --rm -d \
       -p 5000:5000 --net stack_api \
       web_api "$APP_TYPE" "$MODEL_TYPE"
echo "Web_API with '$MODEL_TYPE' and '$APP_TYPE' type started"
