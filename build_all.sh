#!/bin/bash

BASE_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker build -t model_api "$BASE_PATH"/model_api/
echo "Model_API built"
docker build -t db_api "$BASE_PATH"/db_api/
echo "DB_API built"
docker build -t web_api "$BASE_PATH"/web_api/
echo "Web_API built"
echo "Success!"
