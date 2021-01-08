FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa

RUN apt-get update && apt-get -y upgrade

RUN apt-get install -y git

RUN apt-get install -y python3.6 python3.7 python3.8 python-3.9 python3-pip
RUN apt-get install -y python3.6-venv python3.7-venv python3.8-venv python3.9-venv
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN apt-get install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH="/root/.poetry/bin:${PATH}"

RUN apt-get install -y make

# Setup our virtual environments. Sure the intermediate layers are large, but this
# doesn't change often, and can take a while.
#ADD pyproject.toml /src/
#ADD poetry.lock /src/
#WORKDIR /src
#RUN poetry env use 3.6 && poetry install && \
#    poetry env use 3.7 && poetry install && \
#    poetry env use 3.8 && poetry install && \
#    rm -rf /src
