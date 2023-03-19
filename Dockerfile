# syntax=docker/dockerfile:1
FROM python:3-slim

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 444 main.py
RUN chmod 444 requirements.txt

RUN apt-get update && apt-get install -y npm
RUN npm install tailwindcss flowbite
RUN npx tailwindcss init -p
RUN npx tailwindcss -i static/css/main.css -o static/dist/main.css

ENV PORT 8080
ENV FLASK_ENV=production

RUN npm run build:css
# Run the web service on container startup.
CMD [ "waitress-serve", "--port", "8080", "main:create_app" ]