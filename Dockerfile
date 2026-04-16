FROM python:3.12.12-slim-bookworm
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash curl nano mariadb-client git \
    build-essential libssl-dev libffi-dev \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && rm -rf /var/lib/apt/lists/*
ENV PATH="/root/.cargo/bin:${PATH}"
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt
COPY . /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENV FLASK_APP="app:create_app()"
ENV FLASK_DEBUG=1
EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]
