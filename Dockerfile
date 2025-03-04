FROM python:3.13-slim-bookworm
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash curl nano mariadb-client git && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENV FLASK_APP="app:create_app()"
ENV FLASK_DEBUG=1
EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]
