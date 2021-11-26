FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1
RUN mkdir app
WORKDIR /app
COPY requirements.txt /app/
# COPY static/ /app/static/

RUN pip install -r requirements.txt

RUN apt update \
  && apt install -y libpq5 libxml2 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY . .

CMD uwsgi --ini uwsgi.ini