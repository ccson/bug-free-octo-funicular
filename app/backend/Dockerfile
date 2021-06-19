FROM python:3.9-slim-buster

# Set env vars for `pipenv`
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Set the name of the Flask Application
ENV FLASK_APP app

# Creates the source and destination folders for the video transcoding process
RUN mkdir /uploads
RUN mkdir /complete

WORKDIR /app

# Install dependencies
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

# Install `pipenv`
RUN pip3 install pipenv

# Copies over the Python package configuration files
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Installs the Python packages
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install

# Copies the application code to the Docker filesystem
COPY . /app

EXPOSE 80

COPY entrypoint.sh entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
