FROM python:3.11

ENV PYTHONUNBUFFERED 1

# Install MySQL client dependencies and netcat
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential netcat-traditional

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .