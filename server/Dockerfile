FROM python:3.8

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "main:gunicorn_entrypoint", "--bind", "0.0.0.0:8080", "--worker-class", "aiohttp.GunicornWebWorker", "--workers", "2"]
