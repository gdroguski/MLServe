#!/bin/bash

printf "Model_API running: \t%s\n" "$(docker inspect -f "{{.State.Running}}" model_api/)"
printf "DB_API running: \t%s\n" "$(docker inspect -f "{{.State.Running}}" db_api/)"
printf "Web_API running: \t%s\n" "$(docker inspect -f "{{.State.Running}}" web_api/)"
