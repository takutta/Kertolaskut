# syntax=docker/dockerfile:1
FROM python:3.11

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app


RUN chmod 444 main.py
RUN chmod 444 requirements.txt

RUN apt-get update && \
    apt-get install -y npm && \
    npm install tailwindcss flowbite
RUN npx tailwindcss -i ./app/static/src/main.css -o ./app/static/css/main.css
RUN npx tailwindcss -o ./app/static/css/main.css -m
ENV PORT 8080
ENV FLASK_DEBUG 0
ENV FLASK_ENV=production
ENV FLASK_APP=main.py

# Run the web service on container startup.
CMD [ "waitress-serve", "--port", "8080", "main:app" ]