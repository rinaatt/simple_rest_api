FROM python:3.6-slim

RUN apt-get update \
 && apt-get install -y gcc libc6-dev gettext libpq-dev sqlite3 --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 django && useradd -u 1000 -g django django
RUN mkdir /var/rest && chown django:django /var/rest

# USER django:django
VOLUME /var/rest
WORKDIR /var/rest

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -U -r /tmp/requirements.txt
