FROM    python:latest

WORKDIR /usr/local/src

COPY    requirements.txt     requirements.txt
COPY    requirements-dev.txt requirements-dev.txt

RUN     apt update -y                              \
        && apt clean                               \
        && rm -rf /var/lib/apt/lists/*

RUN     pip install --upgrade pip                  \
        && pip install -r requirements.txt         \
        && pip install -r requirements-dev.txt     \
        && pip cache purge

RUN    rm -rf ./*
