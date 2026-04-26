
FROM python:3.12.12-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP="app:create_app()" \
    WORKDIR=/app

WORKDIR $WORKDIR

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    libffi-dev \
    libssl-dev \
    mariadb-client \
    unzip \
    && rm -rf /var/lib/apt/lists/*

FROM base AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM builder AS development

ENV FLASK_DEBUG=1

RUN apt-get update && apt-get install -y --no-install-recommends nano && rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip && ./aws/install && rm -rf awscliv2.zip ./aws

ENV TERRAFORM_VERSION=1.14.9
RUN curl -fsSL -o terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform.zip && mv terraform /usr/local/bin/ && rm terraform.zip

RUN pip install --no-cache-dir /app/wheels/*

COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]

FROM builder AS test

RUN pip install --no-cache-dir ruff pytest

COPY . .
COPY entrypoint.test.sh /entrypoint.test.sh
RUN chmod +x /entrypoint.test.sh

ENTRYPOINT ["/entrypoint.test.sh"]

FROM base AS production

ENV FLASK_DEBUG=0

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY . .

RUN useradd -m flaskuser && chown -R flaskuser:flaskuser /app
USER flaskuser

COPY entrypoint.prod.sh /entrypoint.prod.sh
RUN chmod +x /entrypoint.prod.sh

EXPOSE 5000
ENTRYPOINT ["/entrypoint.prod.sh"]
