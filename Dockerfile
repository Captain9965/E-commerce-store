FROM python:3.8-alpine

ENV PYTHONBUFFERED 1
COPY ./requirements.txt /requirements.txt
#install postgresql-client using alpine's package manager
RUN apk add --update --no-cache postgresql-client jpeg-dev 
RUN apk add --update --no-cache --virtual .tmp-build-deps\
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev\
    libffi-dev
RUN pip3 install -r /requirements.txt
RUN apk del .tmp-build-deps
RUN mkdir /app
COPY ./app /app
WORKDIR /app


