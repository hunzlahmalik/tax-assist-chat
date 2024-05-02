FROM ubuntu:22.04
LABEL authors="ricktorzynski@gmail.com, hunzlahmalik"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update \
  && apt-get -y install tesseract-ocr \
  && apt-get install -y python3 python3-distutils python3-pip \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

RUN apt update \
  && apt-get install ffmpeg libsm6 libxext6 poppler-utils -y

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

WORKDIR /app
COPY . /app


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

EXPOSE 8001
