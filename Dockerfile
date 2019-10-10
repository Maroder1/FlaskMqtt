FROM python:3.7.4-alpine



WORKDIR /home/helloedge

COPY . .
RUN apk update
RUN apk add musl-dev gcc

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python helloedge.py
