FROM python:3.9

RUN apt-get update

WORKDIR /usr/src/
COPY req.txt ./
RUN pip install -r req.txt

COPY . ./

WORKDIR /usr/src/web/
CMD uvicorn main:app --host 0.0.0.0 --port 8000