# syntax=docker/dockerfile:1
FROM python:3-slim

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 444 main.py
RUN chmod 444 requirements.txt

ENV PORT 8080
ENV FLASK_ENV=production
ENV SECRET_KEY=dsaUS2wCS67xsX2ewsdsww23huiWDHdwdwag43ewdJsdjISDuh
ENV GIPHY_API_KEY=zLJPR01eRFGpbQHSjDLnSZlFEZ5FiXEg
RUN npm run build:css
# Run the web service on container startup.
CMD [ "waitress-serve", "--port", "8080", "main:create_app" ]