FROM python:3.9-slim-buster

RUN apt update\
     && apt install -y\
                curl\
                nodejs\
                npm\
    && npm install -g n\
    && n v18.4.0

RUN mkdir -p /code
RUN mkdir -p /code/technologies
RUN mkdir -p /code/templates

COPY react_views /code/react_views
WORKDIR /code/react_views
RUN  npm install --legacy-peer-deps\
     && npm run build

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY *.py /code/
COPY technologies/* /code/technologies/
COPY language_models/ /code/language_models/
# COPY static/ /code/static/
# COPY templates/ /code/templates/
COPY wait-for-it.sh /code/
RUN chmod +x /code/wait-for-it.sh
WORKDIR /code
ENV FLASK_APP=flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN python -m nltk.downloader universal_tagset
RUN python -m nltk.downloader punkt
# CMD python3 flask_app.py
