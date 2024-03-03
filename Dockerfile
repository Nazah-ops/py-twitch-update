FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt update &&\
    apt install ffmpeg -y &&\
    apt-get install build-essential -y &&\
    apt-get install -y wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev &&\
    rm -rf /var/lib/apt/lists/*

#This is for ChromeWebDriver
#RUN apt-get install -y chromium-driver

RUN pip install -r requirements.txt

EXPOSE 8000

CMD jupyter notebook --ip=0.0.0.0 --port=8000 --no-browser --allow-root --NotebookApp.token=''