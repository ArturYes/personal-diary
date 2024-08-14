FROM python:3.11-slim
LABEL authors="Artur"

WORKDIR /app

RUN apt-get update && apt-get install -y curl && apt-get clean

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python manage.py migrate \
    && python manage.py collectstatic --no-input \
