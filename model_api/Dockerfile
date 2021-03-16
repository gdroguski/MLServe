FROM mcr.microsoft.com/azureml/onnxruntime:v1.4.0-cuda10.1-cudnn7
MAINTAINER Grzegorz Roguski

RUN apt-get update && \
	apt-get install -y gcc make apt-transport-https ca-certificates build-essential

RUN python3 --version
RUN pip install --upgrade pip

COPY requirements_docker.txt .
RUN pip install --no-cache-dir -r requirements_docker.txt

COPY app.py .
RUN chmod a+x app.py
RUN mkdir models

EXPOSE 5050

ENTRYPOINT ["python3", "app.py"]
CMD ["mnist"]
