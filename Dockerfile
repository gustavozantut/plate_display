FROM python:3.9
RUN git clone https://github.com/gustavozantut/plate_display /usr/src/app/plate_display/
WORKDIR /usr/src/app/plate_display
RUN apt-get update -y
RUN pip install -r ./requirements.txt
RUN rm ./requirements.txt
ENTRYPOINT ["python", "plate_displayer.py"]
#run
#git pull ; docker build -t guhzantut/plate_display:toll . ; docker run --device /dev/ttyACM0 --rm guhzantut/plate_display:toll