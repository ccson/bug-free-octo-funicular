FROM python:3.9-slim-buster

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV FLASK_APP app

WORKDIR /app

RUN apt-get update -yqq && \
  apt-get upgrade -yqq && \
  apt-get install -yqq --no-install-recommends \
    python3-pip \
    gcc \
    musl-dev \
    libpq-dev \
    libc-dev \
    ffmpeg

RUN pip3 install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install

COPY . /app

EXPOSE 80

CMD ["pipenv", "run", "python3", "-m" , "flask", "run", "--host", "0.0.0.0", "--port", "80"]
