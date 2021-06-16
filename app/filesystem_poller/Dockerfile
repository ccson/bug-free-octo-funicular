FROM python:3.9-slim-buster

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV FLASK_APP app

WORKDIR /app

RUN apt-get update -yqq && \
  apt-get upgrade -yqq && \
  apt-get install -yqq --no-install-recommends \
    python3-pip \
    gcc

RUN pip3 install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install

COPY . /app

CMD ["pipenv", "run", "python3", "main.py"]
