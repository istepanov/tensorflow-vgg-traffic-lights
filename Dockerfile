FROM tensorflow/tensorflow:1.3.0-gpu

WORKDIR /src

RUN apt-get update && apt-get install -y wget zip
RUN pip install PyYAML plumbum
