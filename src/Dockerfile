FROM python:3.9

RUN apt-get update 

ENV DISPLAY :0


COPY . /opt/src

WORKDIR /opt/src

RUN PYTHONPATH=/usr/bin/python pip install -r requirments

RUN gcc launcher.c -o SchoolManager

CMD ./SchoolManager
