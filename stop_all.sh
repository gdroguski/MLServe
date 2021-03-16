#!/bin/bash

docker stop model_api
echo "Model_API stopped"
docker stop db_api
echo "DB_API stopped"
docker stop web_api
echo "Web_API stopped"
