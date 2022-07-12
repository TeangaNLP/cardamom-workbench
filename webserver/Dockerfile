FROM python:3.9-slim-buster

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /code
COPY *.py /code/
COPY static/ /code/static/
COPY templates/ /code/templates/
COPY wait-for-it.sh /code/
RUN chmod +x /code/wait-for-it.sh
WORKDIR /code
ENV FLASK_APP=flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
# CMD python3 flask_app.py
