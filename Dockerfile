FROM python:3

ADD . /

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install poppler-utils -y

CMD [ "python", "./python/main.py" ]