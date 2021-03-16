FROM python:3.8
MAINTAINER Grzegorz Roguski

RUN apt-get update
RUN apt-get install libgl1-mesa-dev -y

RUN python3 --version
RUN pip install --upgrade pip

WORKDIR /usr/src/web_api

COPY requirements_docker.txt .
RUN pip install --no-cache-dir -r requirements_docker.txt

COPY main.sh .
COPY cli_app.py .
COPY ui_app.py .
RUN chmod a+x main.sh
RUN chmod a+x cli_app.py
RUN chmod a+x ui_app.py
EXPOSE 5000


ENTRYPOINT ["./main.sh"]
CMD ["cli", "mnist"]