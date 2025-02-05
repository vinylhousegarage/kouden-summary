FROM python:3.13-slim-bookworm
WORKDIR /app
RUN apt-get update && apt-get install -y bash curl nano
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY app /app/
COPY run.py /app/
ENV FLASK_APP=app:create_app
ENV FLASK_DEBUG=1
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
