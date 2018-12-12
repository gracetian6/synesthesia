FROM ubuntu

EXPOSE 8000

# Install all dependencies
RUN apt-get update && apt-get install -y build-essential git software-properties-common lilypond python3 python3-pip

# Copy project files into /var/www in container
COPY . /var/www

# Change directory inside container to /var/www
WORKDIR /var/www

# Install all Python package dependencies
RUN pip3 install -r requirements.txt

# Starts web server (gunicorn)
# If PORT environment variable is unset, use 8000
CMD gunicorn application:app -b 0.0.0.0:${PORT:-8000}
