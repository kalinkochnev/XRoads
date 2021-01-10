FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/xroads/xroads_dj/bin && mkdir -p /home/xroads/xroads_dj/xroads_django && mkdir -p /home/xroads/xroads_dj/XroadsAPI && mkdir -p /home/xroads/xroads_dj/XroadsAuth

WORKDIR /home/xroads/xroads_dj

COPY ./bin/start_gunicorn.sh /home/xroads/xroads_dj/bin/

COPY ./requirements.txt /home/xroads/xroads_dj/

RUN pip3 install -r /home/xroads/xroads_dj/requirements.txt

COPY ./xroads_django  /home/xroads/xroads_dj/xroads_django/

COPY ./XroadsAPI /home/xroads/xroads_dj/XroadsAPI/

ENTRYPOINT ["/home/xroads/xroads_dj/bin/start_gunicorn.sh"]