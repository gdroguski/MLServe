# DB API container

It's main purpose is to persist data transferred to and from the model from `model_api` for future use and to save some time on unnecessary multiple inferences on the same data.

## How to run this separately:

How to run this manually (if you don't want to ```start_all.sh```):

1. `docker run --name db_api --rm -d \
       --net stack_api \
       --mount type=bind,source="$BASE_PATH"/db_api/data,target=/data \
       db_api`, where `BASE_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"`
2. Now you can play with this redis container as usual. It is just a wrapper within current docker network bridge as said earlier.

To test it run `python ./tests/test_redis.py`. Can be run while `db_api` running separately or with `start_all.sh`