FROM python:3.7-alpine3.11

WORKDIR /usr/src/app/
COPY . ./

RUN pip3 install -r requirements.txt

ENV PYTHONPATH=.
ENV PYTHONUNBUFFERED=1
EXPOSE 5000

CMD python3 ApiGateway/app.py