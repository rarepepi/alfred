FROM python

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

COPY ./alfred /alfred

WORKDIR /alfred
