FROM python:3.13-slim
LABEL org.opencontainers.image.source=https://github.com/OleksiuDatsko/news

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN pip3 install gunicorn

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "app:create_app()"]