FROM python:3.9-slim
WORKDIR /usr/src/app
RUN apt-get update -y
COPY ./ ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN rm requirements.txt
ENTRYPOINT ["python", "plate_displayer.py"]
#run
#git pull ; docker build -t guhzantut/plate_display . ; docker run --device /dev/ttyACM0 --rm guhzantut/plate_display