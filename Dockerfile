# syntax=docker/dockerfile:1
FROM python:3.11

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 444 main.py
RUN chmod 444 requirements.txt

RUN apt-get update && \
    apt-get install -y npm && \
    npm install tailwindcss flowbite
RUN npx tailwindcss init -p
RUN npx tailwindcss -i ./app/static/src/main.css -o ./app/static/css/main.css
ENV PORT 8080
ENV FLASK_ENV=production



# Run the web service on container startup.
CMD ["waitress-serve", "--port", "8080", "main:create_app('$FLASK_CONFIG')"]