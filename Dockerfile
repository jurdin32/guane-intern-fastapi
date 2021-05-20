FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY app/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

CMD ['suvicorn main:app --reload']