FROM python:3.13-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run"]
