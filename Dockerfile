FROM python:3.12-slim-bookworm
WORKDIR /app
ENV TERRAFORM_VERSION=1.14.9
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash curl nano mariadb-client git \
    build-essential libssl-dev libffi-dev \
    unzip \
    && rm -rf /var/lib/apt/lists/*
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip ./aws
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN curl -fsSL -o terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform.zip
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt
COPY . /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENV FLASK_APP="app:create_app()"
ENV FLASK_DEBUG=1
EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]
