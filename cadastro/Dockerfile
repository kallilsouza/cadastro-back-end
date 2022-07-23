FROM python:3.8.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add python3-dev postgresql-dev gcc linux-headers libc-dev

WORKDIR /usr/src/app/

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./entrypoint.sh .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]