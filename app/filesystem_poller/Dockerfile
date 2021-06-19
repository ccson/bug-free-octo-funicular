FROM python:3.9-slim-buster

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
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
    gcc

# Install `pipenv`
RUN pip3 install pipenv

# Copies over the Python package configuration files
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Installs the Python packages
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install

COPY . /app

CMD ["pipenv", "run", "python3", "main.py"]
