FROM python:3.9-slim-buster

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV FLASK_APP app

RUN mkdir /uploads
RUN mkdir /complete

WORKDIR /app

RUN apt-get update -yqq && \
  apt-get upgrade -yqq && \
  apt-get install -yqq --no-install-recommends \
    python3-pip \
    gcc \
    musl-dev \
    libpq-dev \
    libc-dev \
    ffmpeg \
    curl

RUN pip3 install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install

COPY . /app

EXPOSE 80

COPY entrypoint.sh entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
