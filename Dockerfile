FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config build-essential && \
    apt-get clean

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

CMD ["gunicorn", "helloworld_project.wsgi:application", "--bind", "0.0.0.0:80"]
