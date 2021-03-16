#!/bin/bash
APP_TYPE=$1
MODEL_TYPE=$2
if [ "$APP_TYPE" == "ui" ]
then
  echo "Starting APP_TYPE=$APP_TYPE with MODEL_TYPE=$MODEL_TYPE"
#  streamlit run ui_app.py --server.port 5000 --server.headless true --logger.level=debug -- --model "$MODEL_TYPE"
  streamlit run ui_app.py --server.port 5000 --server.headless true -- --model "$MODEL_TYPE"
elif [ "$APP_TYPE" == "cli" ]
then
  echo "Starting APP_TYPE=$APP_TYPE with MODEL_TYPE=$MODEL_TYPE"
  python3 cli_app.py "$MODEL_TYPE"
else
  exit 1
fi
