FROM python:3.9-slim-buster

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /code
COPY *.py /code/
COPY technologies/ /code/technologies/
COPY language_models/ /code/language_models/ 
COPY static/ /code/static/
COPY templates/ /code/templates/
COPY wait-for-it.sh /code/
RUN chmod +x /code/wait-for-it.sh
WORKDIR /code
ENV FLASK_APP=flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN python -m nltk.downloader universal_tagset
RUN python -m nltk.downloader punkt
# CMD python3 flask_app.py
