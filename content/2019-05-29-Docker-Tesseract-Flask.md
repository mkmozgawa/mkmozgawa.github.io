Title: Flask + Tesseract in a Docker container
Date: 2019-05-29 22:00
Modified: 2019-05-29 22:00
Category: Devops
Tags: docker, python, tesseract
Slug: docker-tesseract-flask
Authors: Magda Mozgawa
Summary: A pret-a-porter Dockerfile for Flask apps that use Tesseract, now in Technicolor!

Imagine you have a Flask app with some sort of a model that depends on Tesseract and you want to Dockerize it (because why not?)

...but then it turns out you also have to have Leptonica installed first,

...but it doesn't want to work off apt, so you decide to build it from source,

...but then it turns out that the Leptonica's docs *are not* up to date but you somehow manage to make it work,

...but then it turns out that the Python:3.7 image is built atop Debian Stretch which has Tesseract 3.x in apt and you want Tesseract 4.x.

This is basically the story of this Dockerfile, sans the tears and sweat. Enjoy!

```
FROM python:3.7

RUN echo 'deb http://ftp.debian.org/debian stretch-backports main' > /etc/apt/sources.list.d/backports.list \
    && apt-get dist-upgrade \
    && apt-get update \
    && apt-get install -y \
        make \
        git \
        g++ \
        autoconf automake libtool \
        pkg-config \
        libpng-dev \
        libjpeg62-turbo-dev \
        libtiff5-dev \
        zlib1g-dev \
    && mkdir /install \
    && cd /install \
    && git clone https://github.com/DanBloomberg/leptonica \
    && cd /install/leptonica \
    && ./autogen.sh \
    && ./configure \
    && make \
    && make install \
    && apt -t stretch-backports install -y tesseract-ocr  \
    && apt -t stretch-backports install -y libtesseract-dev

WORKDIR /install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /install/app/
WORKDIR /install/app
CMD ["python", "app.py"]

```

PS so you might ask *why not use Ubuntu:18.04 instead?* to which I say:

1. bloated
2. weird `module Flask cannot be found` issues that took me a while to give up on.