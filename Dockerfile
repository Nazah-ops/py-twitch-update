FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt update &&\
    apt install ffmpeg -y &&\
    apt-get install build-essential -y


RUN pip install -r requirements.txt

EXPOSE 8000

CMD jupyter notebook --ip=0.0.0.0 --port=8000 --no-browser --allow-root --NotebookApp.token=''