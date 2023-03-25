From python:3.8-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ADD m56studios_be /app/

ADD requirements.txt requirements.txt

ADD docker_cmd.sh /app/docker_cmd.sh
ADD docker_cmd_task.sh /app/docker_cmd_task.sh

RUN apk update && apk add --virtual build-deps gcc python3-dev musl-dev && apk add --no-cache mariadb-dev

RUN pip install -r requirements.txt

EXPOSE 8000