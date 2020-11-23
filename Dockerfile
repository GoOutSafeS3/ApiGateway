FROM python:3.7-alpine3.11

WORKDIR /usr/src/app/

COPY requirements.txt ./

RUN pip3 install -r requirements.txt


COPY . ./

ENV PYTHONPATH=.
ENV PYTHONUNBUFFERED=1
EXPOSE 5000

CMD python3 ApiGateway/app.py