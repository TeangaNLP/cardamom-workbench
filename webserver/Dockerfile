FROM python:3.9-slim-buster

RUN apt update\
     && apt install -y\
                curl\
                nodejs\
                npm\
		git\
                ack\
                entr\
    && npm install -g n\
    && n v18.4.0

RUN mkdir -p /code
RUN mkdir -p /code/CorporaUD
RUN mkdir -p /code/technologies
RUN mkdir -p /code/templates

COPY requirements.txt /tmp
# RUN git clone https://github.com/priya-74llh/cardamom_LID.git /code/technologies/cardamom_LID/
# RUN pip install -r /code/technologies/cardamom_LID/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY *.py /code/
COPY CorporaUD /code/CorporaUD/
COPY technologies /code/technologies/
COPY language_models/ /code/language_models/
# COPY static/ /code/static/
# COPY templates/ /code/templates/
COPY wait-for-it.sh /tmp/
RUN chmod +x /tmp/wait-for-it.sh
COPY webserver_run.sh /tmp/
RUN chmod +x /tmp/webserver_run.sh
WORKDIR /code
ENV FLASK_APP=flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN python -m nltk.downloader universal_tagset
RUN python -m nltk.downloader punkt
# CMD python3 flask_app.py

COPY react_views /code/react_views
WORKDIR /code/react_views
RUN  npm install --legacy-peer-deps
#\
#&& npm run build

WORKDIR /code
