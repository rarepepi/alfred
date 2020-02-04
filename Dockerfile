FROM python:3

#Install FreeTDS and dependencies for PyODBC
RUN apt-get update && apt-get install -y tdsodbc unixodbc-dev \
 && apt install unixodbc-bin -y  \
 && apt-get clean -y

RUN echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/arm-linux-gnueabi/odbc/libtdsodbc.so\n\
Setup = /usr/lib/arm-linux-gnueabi/odbc/libtdsS.so" >> /etc/odbcinst.ini

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

COPY ./alfred /alfred

WORKDIR /alfred

CMD python core.py
