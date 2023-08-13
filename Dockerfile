FROM python:3.10-slim-buster

ADD requirements.txt /

RUN python -m pip install -r /requirements.txt

ADD * /
ADD assets /assets

WORKDIR /

EXPOSE 8050

CMD [ "python3", "main.py" ]