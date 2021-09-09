FROM python:3.9

RUN apt-get update

WORKDIR /usr/src/
COPY req.txt ./
RUN pip install -r req.txt

COPY . ./

WORKDIR /usr/src/dramatiq/
CMD python task.py & dramatiq task