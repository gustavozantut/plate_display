FROM python:slim
WORKDIR /usr/src/app
RUN apt-get update -y
RUN apt-get install i2c-tools -y
COPY ./ ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN rm requirements.txt
#ENTRYPOINT ["python", "plate_displayer.py"]