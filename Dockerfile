FROM ubuntu

EXPOSE 8000

RUN apt-get update && apt-get install -y build-essential git software-properties-common lilypond python3 python3-pip
COPY . /var/www
WORKDIR /var/www
RUN pip3 install -r requirements.txt
CMD gunicorn application:app -b 0.0.0.0:${PORT:-8000}
